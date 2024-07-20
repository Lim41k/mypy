
FROM python:3.8

# Создаем директорию
RUN mkdir -p ./test_bot

# Загружаем скрипты и файлы

ADD https://raw.githubusercontent.com/Lim41k/mypy/master/bot.py ./test_bot/bot.py
ADD https://raw.githubusercontent.com/Lim41k/mypy/master/requirements.txt ./test_bot/requirements.txt

COPY .env ./test_bot/.env

# Переходим в рабочую директорию
WORKDIR ./test_bot

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Команда для запуска приложения
CMD ["python", "./bot.py"]


