#!/bin/bash

echo "Прверка наличия Docker"
if command -v docker &>/dev/null; then
echo "Docker установлен"
docker --version
else
    echo "Docker не установлен "
    echo "Идет установка...."
    sudo apt update
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
    sudo apt update
    apt-cache policy docker-ce
    sudo apt install docker-ce
    docker --version
fi
read -p "Введите ваш токен для телеграмм-бота: " token
echo "TOKEN=\"$token\"" > .env
wget https://raw.githubusercontent.com/Lim41k/mypy/master/Dockerfile/Python_bot/Dockerfile -O Dockerfile
docker build -t my_test_bot .
sudo usermod -aG docker $USER
docker run -d --name my_running_bot my_test_bot
rm Dockerfile install_docker.sh .env

