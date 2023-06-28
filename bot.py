#Copyright 2023 socphoenix
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from plemmy import LemmyHttp
import json
import requests
import sys
import time
import re

homeOtShots = 0
awayOtShots = 0
teamID = 0
gamePK = 0
CID = 0
postID = 0
gameOver = False
badServer = True
teamName = ""
#get communityID
def get_communityID():
    request = srv.get_community(None, communityName)
    global CID
    CID = request.json().get("community_view")
    CID = CID["community"].get("id")

# create initial post
def create_post():
    global teamID, gamePK
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

# edit post
def score_update(body2):
    global postID
    test = srv.edit_post(postID, body=body2)

#check for game
def is_game():
    global teamID, gamePK
    game_today = "https://statsapi.web.nhl.com/api/v1/schedule?teamId="
    game_today = game_today + str(teamID)
    r = requests.get(game_today)
    if(r.json().get("totalGames") == 1):
        gamePK = r.json().get("dates")[0].get("games")[0].get("gamePk")
    else:
        print("no game today")
        sys.exit()

#get NHL linescore and other info
def line_score():
    global gameOver
    game_today = "https://statsapi.web.nhl.com/api/v1/game/2022020130/linescore"
    #game_today = "https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/linescore"
    r = requests.get(game_today)
    home_name = r.json().get("teams").get("home").get("team").get("name")
    home_goals = r.json().get("teams").get("home").get("goals")
    home_power = r.json().get("teams").get("home").get("powerPlay")
    home_shots = r.json().get("teams").get("home").get("shotsOnGoal")
    away_name = r.json().get("teams").get("away").get("team").get("name")
    away_goals = r.json().get("teams").get("away").get("goals")
    away_power = r.json().get("teams").get("away").get("powerPlay")
    away_shots = r.json().get("teams").get("away").get("shotsOnGoal")
    currentPeriod = r.json().get("currentPeriod")
    timeLeft = r.json().get("currentPeriodTimeRemaining")
    period = r.json().get("periods")
    body = post_body(away_name, home_name, away_goals, home_goals, away_power, home_power, currentPeriod, timeLeft, period, away_shots, home_shots)
    score_update(body)
    temp = r.json().get("currentPeriodTimeRemaining")
    if(temp == "Final" and currentPeriod >= 3 and away_goals != home_goals):
        gameOver = True


# create post body
def post_body(away_name, home_name, away_goals, home_goals, away_power, home_power, currentPeriod, timeLeft, period, away_shots, home_shots):
    global gamePK, homeOtShots, awayOtShots
    homeOtShots = 0
    awayOtShots = 0
    #overtime handler for current Period stat
    if(currentPeriod >= 4):
        currentPeriod = "OT " + str(currentPeriod - 3)
    numPeriods = len(period) - 1
    #main body
    body = "# " + away_name + " vs " + home_name + " \n"
    body = body + "| Period | Time Remaining | \n"
    body = body + "| ------- | ------------- | \n"
    body = body + "| " + str(currentPeriod) + " | " + timeLeft + " | \n"
    body = body + "## Scores: \n"
    if(numPeriods <= 2):
        body = body + "| Team | Period 1: | Period 2:  | Period 3: | Totals | \n"
        body = body + "| ----- | -------- | ---------- | ----------- | ------| \n"
        body = body + "| " + away_name + " | " +  str(period[0].get("away").get("goals")) + " | "
        body = body +  str(period[1].get("away").get("goals")) + " | " +  str(period[2].get("away").get("goals")) + " | "
        body = body + away_goals + " | \n"
        body = body + "| " + home_name + " | " +  str(period[0].get("home").get("goals")) + " | "
        body = body + str(period[1].get("home").get("goals")) + " | " + str(period[2].get("home").get("goals")) + " | "
        body = body + home_goals + " | \n"
    else:
        body = body + "| Team | Period 1: | Period 2:  | Period 3: | OT | Totals | \n"
        body = body + "| ----- | -------- | ---------- | --------- | ------| ----- | \n"
        body = body + "| " + away_name + " | " +  str(period[0].get("away").get("goals")) + " | "
        body = body +  str(period[1].get("away").get("goals")) + " | " +  str(period[2].get("away").get("goals")) + " | "
        body = body + str(period[numPeriods].get("away").get("goals")) + " | " + str(away_goals) + " | \n"
        body = body + "| " + home_name + " | " +  str(period[0].get("home").get("goals")) + " | "
        body = body + str(period[1].get("home").get("goals")) + " | " + str(period[2].get("home").get("goals")) + " | "
        body = body + str(period[numPeriods].get("home").get("goals")) + " | " + str(home_goals) + " | \n"
    body = body + "## Shots on Goal: \n"
    if(numPeriods <= 2):
        body = body + "| Team | Period 1 | Period 2 | Period 3 | Total Shots | \n"
        body = body + "| ----- | ------- | -------- | -------- | ----------- | \n"
        body = body + "| " + away_name + " | " + str(period[0].get("away").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("away").get("shotsOnGoal")) + " | " + str(period[2].get("away").get("shotsOnGoal")) + " | "
        body = body + str(away_shots) + " | \n"
        body = body + "| " + home_name + " | " + str(period[0].get("home").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("home").get("shotsOnGoal")) + " | " + str(period[2].get("home").get("shotsOnGoal")) + " | "
        body = body + str(home_shots) + " | \n"
    else:
        if(numPeriods - 3 == 0):
            homeOtShots = period[3].get("home").get("shotsOnGoal")
            awayOtShots = period[3].get("away").get("shotsOnGoal")
        else:
            for x in range(3, numPeriods):
                homeOtShots = homeOtShots + period[x].get("home").get("shotsOnGoal")
                awayOtShots = awayOtShots + period[x].get("away").get("shotsOnGoal")
        body = body + "| Team | Period 1 | Period 2 | Period 3 | OT | Total Shots | \n"
        body = body + "| ----- | ------- | -------- | -------- | ---- | ----------- | \n"
        body = body + "| " + away_name + " | " + str(period[0].get("away").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("away").get("shotsOnGoal")) + " | " + str(period[2].get("away").get("shotsOnGoal")) + " | "
        body = body + str(awayOtShots) + " | " + str(away_shots) + " | \n"
        body = body + "| " + home_name + " | " + str(period[0].get("home").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("home").get("shotsOnGoal")) + " | " + str(period[2].get("home").get("shotsOnGoal")) + " | "
        body = body + str(homeOtShots) + " | " + str(home_shots) + " | \n"
    #Power Play status
    body = body + "## Power Play \n"
    body = body + "| Team | On PowerPlay | \n"
    body = body + "| ----- | ------------ | \n"
    body = body + "| " + away_name + " | " + str(away_power) + " | \n"
    body = body + "| " + home_name + " | " + str(home_power) + " | \n"
    return body

#main loop segment
while(badServer == True):
    server = input("enter server (https://server.here): ")
    https = re.compile('^https?://')
    matched = https.match(server)
    if(matched):
        badServer = False
    else:
        print("Bad Server, please make sure you are appending https:// to the server address")
teamID = input("id # of team: ")
teamName = input("name of team: ")
communityName = input("name of local community e.g. flyers: ")
srv = LemmyHttp(server)
badPass = True
while(badPass == True):
        try:
                username = input("user:")
                password = input("pass:")
                output = srv.login(username, password)
                badPass = False
        except:
                print("bad username/password, please try again.")
#is_game()
get_communityID()
create_post()
while(gameOver != True):
    line_score()
    time.sleep(5)
