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
these the script will crash! This script can also make use of a plemmy feature that is not upstream yet. You will need to run: 
> git clone https://github.com/socphoenix/plemmy.git
>
> cd plemmy
>
> git checkout timeout
>
> python setup.py install

Once installed the script will have a timeout feature in case the server is taking too long to respond.

### Run config.py:
> Linux: python3 config.py

>FreeBSD: python3.9 config.py

### Run the bot:
There are 4 scripts here. draft_bot, standings_bot, stat_bot, and bot.py. stat is for team stats, standings are current standings 
around the nhl, a bot.py is for live score updates.

> Linux: python3 bot.py

> FreeBSD: python3.9 bot.py


To see what the bot can currently do, look here: https://enterprise.lemmy.ml/post/416989
