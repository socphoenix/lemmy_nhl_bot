import requests
import sys
import time
from plemmy import LemmyHttp

server = input("Server (include https://) ")
username = input("Username: ")
password = input("Password: ")
communityName = input("Community Name: ")
srv = LemmyHttp(server)
srv.login(username, password)
request = srv.get_community(None, communityName)
CID = request.json().get("community_view")
CID = CID["community"].get("id")
post = srv.create_post(CID, "2023 Draft!", body="")
postID = post.json().get("post_view")
postID = postID["post"].get("id")

r = requests.get("https://statsapi.web.nhl.com/api/v1/draft")
lister = r.json().get("drafts")[0].get("rounds")
teams = lister[0].get("picks")

while(True):
    body = ""
    body2 = ""
    body3 = ""
    body4 = ""
    body5 = ""
    body6 = ""
    body7 = ""
    i = 0
    # Round 1
    j = len(teams)
    body = "# Round 1 \n" + "| Team Name | Pick # | Selection | \n"
    body = body + "| -------- | ------- | -------- |\n"
    while(i < j):
        #print(i)
        #teams[i].get("team")
        body = body + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
        i = i + 1

    #Round 2
    teams = lister[1].get("picks")
    i = 0
    j = len(teams)
    body2 = "# Round 2 \n" + "| Team Name | Pick # | Selection | \n"
    body2 = body2 + "| -------- | ------- | -------- |\n"
    while(i < j):
        body2 = body2 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
        i = i + 1

    #Round 3
    teams = lister[2].get("picks")
    i = 0
    j = len(teams)
    body3 = "# Round 3 \n" + "| Team Name | Pick # | Selection | \n"
    body3 = body3 + "| -------- | ------- | -------- |\n"
    while(i < j):
        body3 = body3 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
        i = i + 1

    #Round 4
    teams = lister[3].get("picks")
    i = 0
    j = len(teams)
    body4 = "# Round 4 \n" + "| Team Name | Pick # | Selection | \n"
    body4 = body4 + "| -------- | ------- | -------- |\n"
    while(i < j):
        body4 = body4 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
        i = i + 1

    #Round 5
    teams = lister[4].get("picks")
    i = 0
    j = len(teams)
    body5 = "# Round 5 \n" + "| Team Name | Pick # | Selection | \n"
    body5 = body5 + "| -------- | ------- | -------- |\n"
    while(i < j):
        body5 = body5 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
        i = i + 1

    #Round 6
    teams = lister[5].get("picks")
    i = 0
    j = len(teams)
    body6 = "# Round 6 \n" + "| Team Name | Pick # | Selection | \n"
    body6 = body6 + "| -------- | ------- | -------- |\n"
    while(i < j):
        body6 = body6 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
        i = i + 1

    #Round 7
    teams = lister[6].get("picks")
    i = 0
    j = len(teams)
    body7 = "# Round 7 \n" + "| Team Name | Pick # | Selection | \n"
    body7 = body7 + "| -------- | ------- | -------- |\n"
    while(i < j):
        body7 = body7 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
        i = i + 1

    #update post
    srv.edit_post(postID, body=body+body2+body3+body4+body5+body6+body7)
    time.sleep(60)
