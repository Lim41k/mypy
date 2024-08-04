#!/bin/bash

# Функция для запроса подтверждения установки
function ask_confirmation() {
    read -p "Вы хотите установить телеграмм-бот? (y/n): " answer
    case ${answer:0:1} in
        y|Y )
            return 0
        ;;
        * )
            return 1
        ;;
    esac
}

# Функция для проверки наличия Python и установки при необходимости
function check_and_install_python() {
    echo "Проверка наличия и установки Python при необходимости"
    sleep 1
    if command -v python3 &>/dev/null; then
        echo "Python уже установлен. Версия: $(python3 --version)"
        sleep 1
    else
        echo "Python не установлен. Устанавливаю Python..."
        sleep 1
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            if [[ -f /etc/debian_version ]]; then
                
                sudo apt install -y python3 python3-pip
            elif [[ -f /etc/redhat-release ]]; then
                sudo yum install -y python3 python3-pip
            elif [[ -f /etc/arch-release ]]; then
                sudo pacman -Syu --noconfirm python python-pip
            elif [[ -f /etc/fedora-release ]]; then
                sudo dnf install -y python3 python3-pip
            else
                echo "Неизвестная версия Linux. Пожалуйста, установите Python вручную."
                exit 1
            fi
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python
        else
            echo "Не поддерживаемая ОС. Пожалуйста, установите Python вручную."
            exit 1
        fi
        echo "Python установлен. Версия: $(python3 --version)"
    fi
}

# Функция для клонирования репозитория с GitHub

function clone_github_repo() {
    echo "----Проверка, установлен ли Git----"
    sleep 1
    if ! command -v git &> /dev/null; then
        echo "Git не установлен. Устанавливаю Git..."
        
        sudo apt install -y git
    fi
    echo "----Git установлен----"
    sleep 1
    # Запрос URL репозитория на GitHub
    read -p "Введите URL репозитория на GitHub: " repo_url
    if [ -z "$repo_url" ]; then
        echo "URL репозитория не может быть пустым."
        exit 1
    fi

    # Клонирование репозитория
    git clone "$repo_url" telegram_bot

    # Переход в директорию репозитория
    if [ -d "telegram_bot" ]; then
        cd telegram_bot || exit
    else
        echo "Ошибка клонирования репозитория."
        exit 1
    fi
}


# Функция для создания файла .env
function create_env_file() {
    read -p "Введите ваш токен для телеграмм-бота: " token
    echo "TOKEN=\"$token\"" > .env
}

# Основной скрипт
if ask_confirmation; then
    sudo apt update
    check_and_install_python
    
    
    
    

    echo "Клонирую репозиторий с GitHub..."
    sleep 1
    clone_github_repo
   
	if [ -f "telegram_bot/requirements.txt" ]; then
    echo "Установка зависимостей из requirements.txt"

    # Попробуем установить зависимости
    pip3 install -r telegram_bot/requirements.txt
    if [ $? -ne 0 ]; then
        echo "Произошла ошибка. Пробуем с опцией --break-system-packages"
        pip3 install -r telegram_bot/requirements.txt --break-system-packages
    fi
    else
        echo "Файл requirements.txt не найден."
    fi
   

    echo "Создаю файл .env..."
    create_env_file

    echo "Установка завершена."
else
    echo "Установка отменена пользователем."
fi



