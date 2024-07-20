#!/bin/bash

sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce

sudo docker --version
read -p "Введите ваш токен для телеграмм-бота: " token
echo "TOKEN=\"$token\"" > .env
wget https://raw.githubusercontent.com/Lim41k/mypy/master/Dockerfile/Dockerfile -O Dockerfile
docker build -t my_test_bot .
docker run -d --name my_running_bot my_test_bot

