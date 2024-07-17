#!/bin/bash


sudo apt install -y python3 python3-pip

pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Произошла ошибка. Пробуем с опцией --break-system-packages"
        pip3 install -r requirements.txt --break-system-packages
    fi
    
read -p "Введите ваш токен для телеграмм-бота: " token
echo "TOKEN=\"$token\"" > .env

python3 bot.py
