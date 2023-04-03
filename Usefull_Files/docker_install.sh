#!/bin/bash

sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://get.docker.com -o /tmp/get-docker.sh && sudo sh /tmp/get-docker.sh && \
    sudo usermod -aG docker $USER && newgrp docker && \
    newgrp docker ; \
    sudo curl -L "github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose && \
    sudo chmod +x /usr/bin/docker-compose