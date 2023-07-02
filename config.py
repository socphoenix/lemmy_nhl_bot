#basic config, will save the token key for future logins, team, community name
import getpass
from plemmy import LemmyHttp
import sqlite3
import requests
import time
import os.path

server = input("server location (use https://): ")
username = input("username: ")
password = getpass.getpass("password: ")
isMod = input("moderator of community? ")
isMod = isMod.lower()

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
    cur.execute("CREATE TABLE user(token, teamID, communityName, server, isMod)")
    cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?);", (token, teamID, communityName, server, isMod))
    con.commit()
except:
    cur.execute("DELETE FROM user")
    cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?);", (token, teamID, communityName, server, isMod))
    con.commit()
try:
    cur.execute("CREATE TABLE schedule(gamePK, date, time)")
    con.commit()
except:
    cur.execute("DELETE FROM schedule")
    con.commit()

#scrape schedule and times, output to database under schedule table
today = time.strftime("%Y")
year = int(today) + 1
t = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=" + str(teamID) + "&season=" + str(today) + str(year))
games = t.json().get("dates")
i = len(games)
j = 0
while(j < i):
    gamePK = games[j].get("games")[0].get("gamePk")
    date = games[j].get("games")[0].get("gameDate")
    date = date.split("T")
    date[1] = date[1].rstrip("Z")
    cur.execute("INSERT INTO schedule VALUES (?, ?, ?);", (gamePK, date[0], date[1]))
    con.commit()
    j = j + 1
