"""Copyright [2023] [socphoenix]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import requests
import sqlite3
from plemmy import LemmyHttp
import os.path
import time
import sys
import post_body

teamID = 0
CID = 0
isMod = "n"
gameOver = False
standings = False
stats = False
postID = 0
teamID = 0
newSchedule = False
srv = ""
# create time based services
# check for game today:

#is game
def isGame():
    global gameOver, games, gamePK, srv, postID
    today = time.strftime("%Y, %m, %d")
    today = str(today)
    today = today.split(", ")
    for x in range(len(games)):
        gameToday = games[x][1]
        gameToday = gameToday.split("-")
        gamePK = games[x][0]
        if(today[0] == gameToday[0] and today[1] == gameToday[1] and today[2] == gameToday[2]):
            timeStart = games[x][2]
            curTime = time.strftime("%H:%M", time.gmtime())
            timeStart = timeStart.split(":")
            curTime = curTime.split(":")
            #compare 0, 1 on these if hour and minute >= to then start game
            if(int(curTime[0]) >= int(timeStart[0]) and int(curTime[1]) >= int(timeStart[1]) and gameOver == False):
                create_post_linescore()
                while(gameOver == False):
                    gameTime()
                srv.feature_post("Community", False, postID)

#create post for linescore
def create_post_linescore():
    global teamID, gamePK, isMod, srv, postID
    #get team Names/date/regular Season
    game_today = "https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/linescore"
    game_today2 = "https://statsapi.web.nhl.com/api/v1/schedule?teamId="
    game_today2 = game_today2 + str(teamID)
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
    posted = False
    while(posted == False):
        try:
            post = srv.create_post(temp, postName, body="")
            postID = post.json().get("post_view")
            postID = postID["post"].get("id")
            posted = True
        except:
            print("failed to post, trying again in 30 seconds")
            time.sleep(30)
    if(isMod == "y"):
        feature = False
        while(feature == False):
            try:
                srv.feature_post("Community", True, postID)
                feature = True
            except:
                print("Failed to feature post, trying again in 30 seconds.")
                time.sleep(30)


#Linescore for game
def gameTime():
    global gameOver, postID, gamePK, srv
    body2, gameOver = post_body.post_body_linescore(gamePK)
    try:
        test = srv.edit_post(postID, body=body2)
    except:
        print("failed to contact server. Adding extra 60 seconds before retrying")
        time.sleep(60)
    time.sleep(5)


#get community ID

def create_post_stats():
    global CID, teamID, srv
    today = time.strftime("%m-%d-%Y")
    title = "Team Stats for the Season as of " + today
    body = post_body.post_body_stats(teamID)
    posted = False
    while(posted == False):
        try:
            srv.create_post(CID, title, body=body)
            posted = True
        except:
            print("failed to post, trying again in 30 seconds.")
            time.sleep(30)

def create_post_standings():
    today = time.strftime("%m-%d-%Y")
    global CID
    postName = "NHL Standings as of " + today
    body = post_body.post_body_standings()
    posted = False
    while(posted == False):
        try:
            post = srv.create_post(CID, postName, body=body)
            posted = True
        except:
            print("failed to post, trying again in 30 seconds.")
            time.sleep(30)

#main loop segment
def daemon():
    global token, communityName, server, teamID, isMod, games, standings, stats, post, CID, newSchedule, gameOver, srv
    dbLocation = os.path.expanduser("~/.cache/lnhl.db")
    if(os.path.exists(dbLocation) == False):
        print("Please run config.py first!")
        sys.exit()

    #sql database connection/data grabbing
    con = sqlite3.connect(dbLocation)
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
    request = srv.get_community(None, communityName)
    global CID
    CID = request.json().get("community_view")
    CID = CID["community"].get("id")


    #main loop
    while(True):
        isGame()
        today = time.strftime("%a")
        if(str(today) == "Sun" and standings == False):
            create_post_standings()
            create_post_stats()
            standings = True
            stats = True
            newSchedule = True
            # get new schedule weekly to catch playoffs
            cur.execute("DELETE FROM schedule")
            con.commit()
            year = int(time.strftime("%Y"))
            t = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=" + str(teamID) + "&season=" + str(year) + str(year + 1))
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
            r = cur.execute("SELECT * FROM schedule")
            games = r.fetchall()
        elif(str(today) == "Tue" and standings == True):
            standings = False
            stats = False
            newSchedule = False
        time.sleep(300)
