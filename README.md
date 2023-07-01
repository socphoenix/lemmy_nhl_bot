# DEV BRANCH WILL BE UNSTABLE! PUSHES TO DEV WILL BE FOCUSED ON CREATING A DAEMON AND LIKELY WILL NOT WORK WHILE THIS IS IN PROGRESS!


# lemmy_nhl_bot
nhl linescore grabber/poster for lemmy

This script requires the following to be installed from pip: plemmy, requests, json

> pip install plemmy  # source is https://github.com/tjkessler/plemmy/  Many thanks for tjkessler for the simple to use library!

> pip install requests

> pip install json

This has been tested with python 3.9 in FreeBSD and python3 in linux for a few basic outputs. Will be testing it on the first preseason game for live updates and pushing any needed fixes at that time in preperation for the regular season.

This bot is still a work in progress. Right now it needs username/password/server to be entered each time it is run. it also requires the integer teamID from the nhl api. Future update will be able to scrape this info. Bot refreshes the line score every five seconds and updates the post body with basic score. Period info to be added later.

## Usage:
Before starting bot.py, please make sure to run config.py! It is needed to save your login token and teamID/community Name. Without
these the script will crash!

### Run config.py:
> Linux: python3 config.py

>FreeBSD: python3.9 config.py

### Run the bot:
There are 2 scripts here. draft_bot, lemmy_nhl_bot.py. draft_bot currently needs to be run manually each day of the draft. lemm_nhl_bot.py is
meant to act as a daemon and be run continuously. It will pull from config.py for information needed during the season.

> Linux: python3 lemmy_nhl_bot.py (to detach this from the console screen so you can close it, add " &" to the command)

> FreeBSD: python3.9 lemm_nhl_bot.py (to detach this from the console screen so you can close it, add " &" to the command)

### Current Testing:
daemon.py is currently in testing for running as a service. There is no guarantee it will work, will have more information in a few days on this once testing is done.


To see what the bot can currently do, look here: https://enterprise.lemmy.ml/post/416989
