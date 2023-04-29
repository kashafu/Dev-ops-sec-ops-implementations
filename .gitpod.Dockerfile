FROM gitpod/workspace-full:latest

USER gitpod

RUN sudo apt-get update \
 && sudo apt-get install -y \
  redis-server \
 && sudo rm -rf /var/lib/apt/lists/*

ADD requirements.txt .
ADD requirements-dev.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt