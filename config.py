#basic config, will save the token key for future logins, team, community name
import getpass
from plemmy import LemmyHttp
import sqlite3

print("Basic Setup, This will store your auth token in an unencrypted database. Username/password itself are not saved.")
server = input("server address (make sure to include the https://): ")
username = input("Username: ")
password = getpass.getpass('Password: ')
teamID = input("Team ID NUM: ")
communityName = input("Name of the local community: ")

srv = LemmyHttp(server)
r = srv.login(username, password)
token = r.json().get("jwt")

con = sqlite3.connect("lnhl.db")
cur = con.cursor()
cur.execute("CREATE TABLE user(token, teamID, communityName)")
cur.execute("INSERT INTO user VALUES (?, ?, ?);", (token, teamID, communityName))
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
