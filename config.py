#basic config, will save the token key for future logins, team, community name
import getpass
from plemmy import LemmyHttp
import sqlite3
import requests

print("Basic Setup, This will store your auth token in an unencrypted database. Username/password itself are not saved.")
print("If database already exists all data will be overwritten!")
server = input("server address (make sure to include the https://): ")
communityName = input("Name of local Community")
username = input("Username: ")
password = getpass.getpass('Password: ')
isMod = input("Is this account a mod of the community? (needed to pin posts) (y/n): ")

t = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
teams = t.json().get("teams")
print("Select team Number from the following:")

for x in range(0, len(teams)):
    print(teams[x].get("name") + ": " + str(teams[x].get("id")))
teamID = input("Team ID NUM: ")
communityName = input("Name of the local community: ")

srv = LemmyHttp(server)
r = srv.login(username, password)
token = r.json().get("jwt")

con = sqlite3.connect("lnhl.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE user(token, teamID, communityName)")
    cur.execute("INSERT INTO user VALUES (?, ?, ?, ?);", (token, teamID, communityName, isMod))
    con.commit()
except:
    cur.execute("DELETE FROM user")
    cur.execute("INSERT INTO user VALUES (?, ?, ?, ?);", (token, teamID, communityName, isMod))
    con.commit()


#in bot.py will need to use l/rstrip as follow for token:
# r = cur.execute("SELECT token FROM user")
# token = r.fetchall()
# token2 = str(token[0])
# token2 = token2.lstrip("('")
# token2 = token2.rstrip("',)")

# r = cur.execute("SELECT communityName FROM user")
# test = r.fetchall()
# test = str(test[0])
# test.lstrip("('")
# test.rstrip("',)")

#on bot.py srv.key = token2
