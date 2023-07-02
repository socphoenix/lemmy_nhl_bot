# lemmy_nhl_bot
nhl linescore grabber/poster for lemmy

## Docker install
This branch is for docker installs. you will need to download the "Dockerfile" and "config.py" to a directory.
Run 
> python3 config.py

then run:
> docker build --pull -t lemmy-nhl .
>
> docker run lemmy-nhl &

it's not pretty but it does work.

The docker container cannot run the draft bot!

To see what the bot can currently do, look here: [pinned game](https://enterprise.lemmy.ml/post/417088), [stats](https://enterprise.lemmy.ml/post/417090), [standings](https://enterprise.lemmy.ml/post/417089)
