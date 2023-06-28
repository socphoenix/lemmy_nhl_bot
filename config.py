#basic config, will save the token key for future logins, team, community name
import getpass
from plemmy import LemmyHttp
import sqlite3

print("Basic Setup, This will store your auth token in an unencrypted database.")
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
cur.execute("CREATE TABLE user(token, teamID, comunityName)")
cur.execute("INSERT INTO user VALUES (?, ?, ?);", (token, teamID, communityName))
con.commit()
