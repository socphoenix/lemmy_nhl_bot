# A few things to note currently:

> Without modifying files, there is currently no way to test this. I've tested that it works with old data, and will be testing/
> fixing whatever needs it during the first preseason game of the Flyers (or earlier if someone reports an issue before this).


# lemmy_nhl_bot

nhl linescore grabber/poster for lemmy. This app is meant to be run in the background to routinely add scores, standings, and team
stats to a lemmy community focusing on a specific hockey team (standings are league wide, as is the draft function). After being
configured, the main app is run in the background. It will check weekly for an updated schedule. Once per week
(currently set to Sunday), it will post an updated League-wide standings page, and an updated team stats page. Once game days, it
will start automatically at game time, and post scores and time updates every five seconds.


# Docker image

There is a [branch](https://github.com/socphoenix/lemmy_nhl_bot/tree/docker) of this repo to aid in building a Docker image.
To build and install with docker:

> Download the following to a directory:
> (these are available on the release page beginning with 1.5.1)
> [Dockerfile](https://github.com/socphoenix/lemmy_nhl_bot/blob/c056d557951d1e9bae1ab602c22b9e5b7788c03b/Dockerfile)
> [config.py](https://github.com/socphoenix/lemmy_nhl_bot/blob/c056d557951d1e9bae1ab602c22b9e5b7788c03b/config.py)
>
> run:
>
> python3 config.py
>
> docker build -t lemmy_nhl_bot .


# Building:

    This script requires the following to be installed from pip: plemmy, requests, json

> pip install plemmy   source is https://github.com/tjkessler/plemmy/  Many thanks for tjkessler for the simple to use library!

> pip install requests

> pip install json


## Build the .whl
> git clone https://github.com/socphoenix/lemmy_nhl_bot.git
>
> cd lemmy_nhl_bot
>
> git checkout dev
>
> Linux (FreeBSD use python3.9): python3 -m build . --wheel
>
> cd dist
>
> pip install lemmy_nhl-2.0.0-py3-none-any.whl

## Usage:
Before starting bot.py, please make sure to run config.py! It is needed to save your login token and teamID/community Name. Without
these the script will crash!

### Run config.py:
> Linux: lemmy_nhl_config

>FreeBSD: lemmy_nhl_config.py ##This requires path set. for sh (default shell): "PATH=${PATH}:/home/'put user here'/.local/bin" "export PATH" (as an interesting note, python seems to only add the path to the root user during install)

### run daemon

Linux:
 > daemonize lemmy_nhl_daemon
 >
 > FreeBSD:
 > daemon lemmy_nhl_daemon

### run draft bot

Unix: lemmy_nhl_draft


# See it in action!

To see what the bot can currently do, look here: [pinned game](https://enterprise.lemmy.ml/post/417088), [stats](https://enterprise.lemmy.ml/post/417090), [standings](https://enterprise.lemmy.ml/post/417089)


# Shared Libraries

This uses the [Plemmy](https://github.com/tjkessler/plemmy/) library, which is also released under the Apache 2.0 license.
Many thanks to tjkessler for the simple to use library!
