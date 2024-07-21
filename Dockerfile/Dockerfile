FROM python:3.8

# Создаем директорию
RUN mkdir -p /app/test_bot

# Копируем .env файл в контейнер
COPY .env /app/test_bot/.env

# Загружаем скрипты и файлы
ADD https://raw.githubusercontent.com/Lim41k/mypy/master/bot.py /app/test_bot/bot.py
ADD https://raw.githubusercontent.com/Lim41k/mypy/master/requirements.txt /app/test_bot/requirements.txt

# Переходим в рабочую директорию
WORKDIR /app/test_bot

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Команда для запуска приложения
CMD ["python", "./bot.py"]
