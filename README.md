# lemmy_nhl_bot
nhl linescore grabber/poster for lemmy

This script requires the following to be installed from pip: plemmy, requests, json
pip install plemmy
pip install requests
pip install json

This bot is still a work in progress. Right now it needs username/password/server to be entered each time it is run. it also requires the integer teamID from the nhl api. Future update will be able to scrape this info. Bot refreshes the line score every five seconds and updates the post body with basic score. Period info to be added later.
