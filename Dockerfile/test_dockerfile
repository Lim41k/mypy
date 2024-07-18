FROM python:3.8

RUN mkdir -p ./test_bot
COPY https://raw.githubusercontent.com/Lim41k/mypy/master/Dockerfile/test.py -O test.py .
# ADD https://raw.githubusercontent.com/Lim41k/mypy/master/bot.py -O bot.py /test_bot
# ADD https://raw.githubusercontent.com/Lim41k/mypy/master/requirements.txt -O bot.py /test_bot


# WORKDIR /test_bot

# RUN bash i_bot.sh

CMD [ "python", "./test.py" ]