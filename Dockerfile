FROM ubuntu:latest

# intsall python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# install nodejs
RUN apt-get update && apt-get install -y nodejs

# install npm
RUN apt-get update && apt-get install -y npm

# install docker
RUN apt-get install -y \
    ca-certificates \
    curl \
    gnupg

RUN mkdir -m 0755 -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update

RUN apt-get install -y docker-ce docker-ce-cli containerd.io

# install github cli
RUN type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y) curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y 

# install requirements from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# copy the app
RUN mkdir /app
RUN mkdir /app/scripts
RUN mkdir /app/configs
RUN mkdir /app/builds
RUN mkdir /app/secret

WORKDIR /app

COPY src src

# run the app
CMD ["gunicorn", "-w", "4", "'src.server.app:app'"]

