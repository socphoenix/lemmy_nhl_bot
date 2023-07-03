FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip git python3-venv
RUN pip install requests && pip install plemmy && pip install build
RUN git clone https://github.com/socphoenix/lemmy_nhl_bot.git && cd lemmy_nhl_bot && \
git checkout docker
RUN cd lemmy_nhl_bot && python3 -m build . --wheel && cd dist && pip install lemmy_nhl-1.5.3-py3-none-any.whl
COPY lnhl.db /opt/lnhl.db
CMD lemmy_nhl_daemon 
