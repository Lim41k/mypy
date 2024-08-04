import requests

# Замените на ваш токен бота
TOKEN = 'TOKEN'
# Замените на ID вашего сервера (гильдии)
GUILD_ID = 'Your ID'

url = f'https://discord.com/api/guilds/{GUILD_ID}/members?limit=1000'

payload = {}
headers = {'Authorization': f'Bot {TOKEN}'}
response = requests.request("GET", url, headers=headers, data=payload)
      
def find_user_by_username(username):
    for member in response.json():
        if member['user']['username'] == username:
            return member['user']['username']
    return None

print(find_user_by_username("limchik_47151"))

print(find_user_by_username("limchik"))