from plemmy import LemmyHttp
import json
import requests
import sys
import time
import sqlite3
import os.path

teamID = 0
CID = 0
def post_body():
    global teamID
    link = "https://statsapi.web.nhl.com/api/v1/teams/" + str(teamID) + "/stats"
    r = requests.get(link)
    team = r.json().get("stats")[1].get("splits")[0].get("team").get("name")
    stats = []
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("ptPctg"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("goalsPerGame"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("goalsAgainstPerGame"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("powerPlayPercentage"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("penaltyKillPercentage"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("shotsPerGame"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("shotsAllowed"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("faceOffWinPercentage"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("shootingPctg"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("savePctg"))
    i = len(stats)
    j = 0
    body = "| Pnt Pctge | Goals Per Game | Goals Against Per Game | Power Play % | Penalty Kill % | Shots Per Game | Shots Allowed | "
    body = body + "Face Off Win % | Shooting % | Save % |\n"
    body = body + "| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | \n"
    body = body + "| " + str(stats[0]) + " | " + str(stats[1]) + " | " + str(stats[2]) + " | " + str(stats[3]) + " | "
    body = body + str(stats[4]) + " | " + str(stats[5]) + " | " + str(stats[6]) + " | " + str(stats[7]) + " | "
    body = body + str(stats[8]) + " | " + str(stats[9]) + " | \n"
    return body

def get_communityID(communityName):
    request = srv.get_community(None, communityName)
    global CID
    CID = request.json().get("community_view")
    CID = CID["community"].get("id")

def create_post():
    global CID
    today = time.strftime("%m-%d-%Y")
    title = "Team Stats for the Season as of " + today
    body = post_body()
    srv.create_post(CID, title, body=body)

#start main program
if(os.path.exists('lnhl.db') == False):
    print("Please run config.py first!")
    sys.exit()

#sql database connection/data grabbing
con = sqlite3.connect("lnhl.db")
cur = con.cursor()
#get login token
r = cur.execute("SELECT token FROM user")
temp = r.fetchall()
token = str(temp[0])
token = token.lstrip("('")
token = token.rstrip("',)")
#get community Name
r = cur.execute("SELECT communityName FROM user")
temp = r.fetchall()
communityName = str(temp[0])
communityName = communityName.lstrip("('")
communityName = communityName.rstrip("',)")
# get server name
r = cur.execute("SELECT server FROM user")
temp = r.fetchall()
server = str(temp[0])
server = server.lstrip("('")
server = server.rstrip("',)")
srv = LemmyHttp(server)
srv.key = token
# get teamID
r = cur.execute("SELECT teamID FROM user")
temp = r.fetchall()
teamID = str(temp[0])
teamID = teamID.lstrip("('")
teamID = teamID.rstrip("',)")

#get community name then create post
get_communityID(communityName)
create_post()

