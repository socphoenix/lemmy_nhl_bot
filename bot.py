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

teamID = 0
gamePK = 0
communityID = 0
postID = 0
gameOver = false

#main loop segment
server = input("enter server (https://server.here): ")
username = input("enter username: ")
password = input("enter password: ")
teamID = input("id # of team: ")
communityName = input("name of local community e.g. flyers: ")
srv = LemmyHttp(server)
srv.login(username, password)
is_game()
get_communityID()
create_post()
while(gameOver != true):
    line_score()
    time.sleep(5)
    

#get communityID
def get_communityID():
    request = srv.get_community(None, communityName)
    communityID = request.json().get("community_view")
    communityID = communityID["community"].get("id")

# create initial post
def create_post():
    post = srv.create_post(communityID, "Game_Name", body="body")
    postID = post.json().get("post_view")
    postID = postID["post"].get("id")

# edit post
def score_update(body):
    srv.edit_post(postID, body="edited")

#check for game
def is_game():
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
    game_today = "https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/linescore"
    r = requests.get(game_today)
    home_name = r.json().get("teams").get("home").get("team").get("name")
    home_goals = r.json().get("teams").get("home").get("goals")
    home_power = r.json().get("teams").get("home").get("powerPlay")
    home_shots = r.json().get("teams").get("home").get("shotsOnGoal")
    away_name = r.json().get("teams").get("home").get("team").get("name")
    away_goals = r.json().get("teams").get("home").get("goals")
    away_power = r.json().get("teams").get("home").get("powerPlay")
    away_shots = r.json().get("teams").get("home").get("shotsOnGoal")
    currentPeriod = r.json().get("currentPeriod")
    body = post_body(away_name, home_name, away_goals, home_goals, away_power, home_power, currentPeriod)
    score_update(body)
    if(r.json().get("currentPeriodTimeRemaining") == "Final"):
        gameOver = true
    

# create post body
def post_body(away_name, home_name, away_goals, home_goals, away_power, home_power, currentPeriod):
    body = "Current Period: " + str(currentPeriod) + "\n" + "away_name + ": " + away_goals + "  Powerplay: " + away_power + "\n" 
    body = body + home_name + ": " + home_goals + " Powerplay: " + home_power
    return body