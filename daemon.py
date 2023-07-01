import requests
import sqlite3
from plemmy import LemmyHttp
import os.path
import time
import body

teamID = 0
CID = 0
isMod = "n"
gameOver = False
standings = False
stats = False
postID = 0
teamID = 0

# create time based services
# check for game today:
def isGame():
    global gameOver
    today = time.strftime("%Y, %m, %d")
    today = str(today)
    today = today.split(", ")
    for x in range(len(games)):
        gameToday = games[x][1]
        gameToday = gameToday.split("-")
        if(today[0] == gameToday[0] and today[1] == gameToday[1] and today[2] == gameToday[2]):
            timeStart = x[0][2]
            curTime = time.strftime("%H:%M", time.gmtime())
            timeStart = timeStart.split(":")
            curTime = curTime.split(":")
            #compare 0, 1 on these if hour and minute >= to then start game
            if(int(curTime[0]) >= int(timeStart[0]) and int(curTime[1]) >= int(timeStart[1]) and gameOver == False):
                   create_post_linescore()
                   while(gameOver == False):
                       gameTime()

#create post for linescore
def create_post_linescore():
    global teamID, gamePK, isMod
    #get team Names/date/regular Season
    game_today = "https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/linescore"
    game_today2 = "https://statsapi.web.nhl.com/api/v1/schedule?teamId="
    game_today2 = game_today + str(teamID)
    r = requests.get(game_today)
    t = requests.get(game_today2)
    home_name = r.json().get("teams").get("home").get("team").get("name")
    away_name = r.json().get("teams").get("away").get("team").get("name")
    date = t.json().get("dates")[0].get("date")
    gameType = t.json().get("dates")[0].get("games")[0].get("gameType")
    if(gameType == "R"):
        gameType = "Regular Season"
    elif(gameType == "PR"):
        gameType = "Pre-Season"
    else:
        gameType = "Playoffs"
    postName = away_name + " vs. " + home_name + " " + gameType + " " + str(date)
    global CID, postID
    temp = CID
    post = srv.create_post(temp, postName, body="")
    postID = post.json().get("post_view")
    postID = postID["post"].get("id")
    if(isMod == "y"):
        srv.feature_post("Community", True, postID)


#Linescore for game
def gameTime():
    global gameOver, postID, gamePK
    body2, gameOver = body.post_body_linescore(gamePK)
    try:
        test = srv.edit_post(postID, body=body2)
    except:
        print("failed to contact server. Adding extra 60 seconds before retrying")
        time.sleep(60)
    sleep(5)


#get community ID
def get_communityID(communityName):
    request = srv.get_community(None, communityName)
    global CID
    CID = request.json().get("community_view")
    CID = CID["community"].get("id")


#create post, will need to edit
def create_post_linescore():
    global teamID, gamePK, isMod
    #get team Names/date/regular Season
    game_today = "https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/linescore"
    game_today2 = "https://statsapi.web.nhl.com/api/v1/schedule?teamId="
    game_today2 = game_today + str(teamID)
    r = requests.get(game_today)
    t = requests.get(game_today2)
    home_name = r.json().get("teams").get("home").get("team").get("name")
    away_name = r.json().get("teams").get("away").get("team").get("name")
    date = t.json().get("dates")[0].get("date")
    gameType = t.json().get("dates")[0].get("games")[0].get("gameType")
    if(gameType == "R"):
        gameType = "Regular Season"
    elif(gameType == "PR"):
        gameType = "Pre-Season"
    else:
        gameType = "Playoffs"
    postName = away_name + " vs. " + home_name + " " + gameType + " " + str(date)
    global CID, postID
    temp = CID
    post = srv.create_post(temp, postName, body="")
    postID = post.json().get("post_view")
    postID = postID["post"].get("id")
    if(isMod == "y"):
        srv.feature_post("Community", True, postID)

def create_post_stats():
    global CID, teamID
    today = time.strftime("%m-%d-%Y")
    title = "Team Stats for the Season as of " + today
    body = body.post_body_stats(teamID)
    srv.create_post(CID, title, body=body)

def create_post_standings():
    today = time.strftime("%m-%d-%Y")
    global CID
    postName = "NHL Standings as of " + today
    body = body.post_body_standings()
    post = srv.create_post(CID, postName, body=body)

#main loop segment
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
#get teamID
r = cur.execute("SELECT teamID FROM user")
temp = r.fetchall()
teamID = str(temp[0])
teamID = teamID.lstrip("('")
teamID = teamID.rstrip("',)")

#get mod status
r = cur.execute("SELECT isMod FROM user")
temp = r.fetchall()
isMod = str(temp[0])
isMod = isMod.lstrip("('")
isMod = isMod.rstrip("',)")

#get games
r = cur.execute("SELECT * FROM schedule")
games = r.fetchall()

#use login token, check for game, get community id, create post, then loop
srv = LemmyHttp(server)
srv.key = token
get_communityID(communityName)

#main loop
while(True):
    isGame()
    today = time.strftime("%a")
    if(str(today) == "Mon" and standings == False):
        create_post_standings()
        create_post_stats
        standings = True
        stats = True
    elif(str(today) == "Tue" and standings == True):
        standings = False
        stats = False
    time.sleep(300)
