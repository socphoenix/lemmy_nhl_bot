# lemmy_nhl_bot
nhl linescore grabber/poster for lemmy

This script requires the following to be installed from pip: plemmy, requests, json

> pip install plemmy  # source is https://github.com/tjkessler/plemmy/  Many thanks for tjkessler for the simple to use library!

> pip install requests

> pip install json

This has been tested with python 3.9 in FreeBSD and python3 in linux for a few basic outputs. Will be testing it on the first preseason game for live updates and pushing any needed fixes at that time in preperation for the regular season.


## Install from pip
> pip install lemmy-nhl==1.5.0

## Install using Docker:
See [docker branch](https://github.com/socphoenix/lemmy_nhl_bot/tree/docker) of repo, there is a config.py script that needs to be run 
before docker build!

## Usage:
Before starting bot.py, please make sure to run config.py! It is needed to save your login token and teamID/community Name. Without
these the script will crash!


### Run config.py:
> Linux: lemmy_nhl_config

>FreeBSD: lemmy_nhl_config ##This requires path set. for sh (default shell): "PATH=${PATH}:/home/'put user here'/.local/bin" "export PATH"

### run daemon
Unix: lemmy_nhl_daemon   **** add " &" to run in the background.


### run draft bot
Unix: lemmy_nhl_draft



To see what the bot can currently do, look here: [pinned game](https://enterprise.lemmy.ml/post/417088), [stats](https://enterprise.lemmy.ml/post/417090), [standings](https://enterprise.lemmy.ml/post/417089)
