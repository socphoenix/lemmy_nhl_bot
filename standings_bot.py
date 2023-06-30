from plemmy import LemmyHttp
import json
import requests
import sys
import sqlite3
import os.path
import time

CID = 0
postID = 0

#create post body
def post_body():
    r = requests.get("https://statsapi.web.nhl.com/api/v1/standings")
    teams = r.json().get("records")[0].get("teamRecords")
    i = 0
    j = len(teams)
    body = "# Eastern Conference \n\n ## Metropolitan Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs | \n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- | \n"
    while(i < j):
        team = r.json().get("records")[0].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[0].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[0].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[0].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[0].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[0].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    teams = r.json().get("records")[1].get("teamRecords")
    i = 0
    j = len(teams)
    body = body + "## Atlantic Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs |\n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- |\n"
    while(i < j):
        team = r.json().get("records")[1].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[1].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[1].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[1].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[1].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[1].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    #3rd
    teams = r.json().get("records")[2].get("teamRecords")
    i = 0
    j = len(teams)
    body = body + "# Western Conference \n\n ## Central Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs |\n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- |\n"
    while(i < j):
        team = r.json().get("records")[2].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[2].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[2].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[2].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[2].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[2].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    #4th
    teams = r.json().get("records")[3].get("teamRecords")
    i = 0
    j = len(teams)
    body = body + "## Pacific Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs |\n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- |\n"
    while(i < j):
        team = r.json().get("records")[3].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[3].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[3].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[3].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[3].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[3].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    return body

#get community ID
def get_communityID(communityName):
    request = srv.get_community(None, communityName)
    global CID
    CID = request.json().get("community_view")
    CID = CID["community"].get("id")

# create initial post
def create_post():
    today = time.strftime("%m-%d-%Y")
    global CID, postID
    temp = CID
    postName = "NHL Standings as of " + today
    body = post_body()
    post = srv.create_post(temp, postName, body=body)


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
get_communityID(communityName)
create_post()
