import os  
import asyncio  
import random  
import string  
import aiohttp  
from aiohttp import ClientConnectorError  
from pyfiglet import Figlet  
import time
from flask import Flask
from threading import Thread

# Credits to GOD  
print("Credits to @We_areGOD ")  
print()  
  
# Colors  
green_console = "\033[92m"  
red_console = "\033[91m"  
yellow_console = "\033[93m"  
  
# Banner  
print("\033[1;33;40m  ~ Pяσɢяαммεя • @We_areGOD • -> @We_areGOD |  ~")  
print("\x1b[1;39m", "_" * 55, '\n')  
  
# Logo  
fig = Figlet(font='slant')  
logo = fig.renderText('Hex-5L')  
print("\033[1;36;40m")  
print(logo)  
  
# Rare 4L usernames  
custom_usernames = [  
    'krpt', 'bldz', 'vlnt', 'grmz', 'znqx', 'qvrn', 'trxz', 'clvx',  
    'vnsh', 'drkm', 'blxz', 'xqrv', 'zjtx', 'nqst', 'jvxl', 'xrmz'  
]  
  
# Telegram bot info  
token = "7654568456:AAFvwVhXT3dWtjlA32ZugTpVH1Ol3cC4vD0"  
telegram_user_id = "7834524112"  
  
# Keep-alive counter
request_count = 0

# Flask uptime server
app = Flask(__name__)

@app.route('/')
def home():
    return f"Username Checker is running! Requests processed: {request_count}"

@app.route('/ping')
def ping():
    return "pong"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Start Flask server in a separate thread
Thread(target=run_flask, daemon=True).start()
print(f"{yellow_console}🌐 Uptime server started on port 10000")

# Username Generator  
async def generate_username(username_type='4A'):  
    if username_type == '4A':  
        chars = string.ascii_lowercase + string.digits + '_.'
        return ''.join(random.choice(chars) for _ in range(4))  
  
# Save available usernames  
def save_username_to_file(username):  
    with open("available.txt", "a") as f:  
        f.write(username + "\n")  
  
# Telegram notifier  
async def send_telegram_message(username):  
    while True:  
        try:  
            async with aiohttp.ClientSession() as s:  
                await s.get(f"https://api.telegram.org/bot{token}/sendMessage",  
                            params={"chat_id": telegram_user_id, "text": f"🔥 Username Available: {username}"})  
            break  
        except ClientConnectorError:  
            print(f"{yellow_console}⚠ no internet... waiting to reconnect for telegram...")  
            await asyncio.sleep(5)  
  
# Create account checker with retry  
async def create_instagram_account(session, username_type):  
    global request_count
    while True:  
        username = await generate_username(username_type)  
        headers = {  
            "Host": "i.instagram.com",  
            "cookie": "mid=Y16iBgABAAFggfUYwajggkGFz-hs",  
            "x-ig-capabilities": "AQ==",  
            "cookie2": "$Version=1",  
            "x-ig-connection-type": "WIFI",  
            "user-agent": "Instagram 6.12.1 Android",  
            "content-type": "application/x-www-form-urlencoded",  
            "accept-encoding": "gzip"  
        }  
        data = {  
            "password": "zxcvbm1@",  
            "device_id": "android-2793e055-2a92-4df2-890f-f88f52538de5",  
            "guid": "2793e055-2a92-4df2-890f-f88f52538de5",  
            "email": "zodhokxbsbdbsbsksbs@gmail.com",  
            "username": username  
        }  
  
        while True:  
            try:  
                async with session.post("https://i.instagram.com/api/v1/accounts/create/", headers=headers, data=data) as res:  
                    request_count += 1
                    if request_count % 50 == 0:
                        print(f"{yellow_console}🔄 Keep-alive: {request_count} requests processed")
                    
                    if 'application/json' in res.headers.get('Content-Type', ''):  
                        j = await res.json()  
                        error = j.get('error_type')  
                        if error == 'needs_upgrade':  
                            print(f'{green_console}✅ Available: {username}')  
                            await send_telegram_message(username)  
                            save_username_to_file(username)  
                        elif error == 'taken':  
                            print(f'{red_console}❌ Taken: {username}')  
                        else:  
                            print(f'{yellow_console}⚠️ {error}: {username}')  
                    else:  
                        print(f'{yellow_console}⚠️ Non-JSON Response: {await res.text()}')  
                    break  
            except ClientConnectorError:  
                print(f"{yellow_console}⚠ internet disconnected... retrying request...")  
                await asyncio.sleep(5)  
            except Exception as e:  
                print(f'{red_console}Error: {e}')  
                await asyncio.sleep(2)
                break  
  
# Rare check with internet retry  
async def check_rare_usernames():  
    while True:  
        try:  
            async with aiohttp.ClientSession() as session:  
                while True:  
                    tasks = []  
                    for u in custom_usernames:  
                        url = f'https://www.instagram.com/{u}/'  
                        headers = {'User-Agent': 'Mozilla/5.0'}  
                        task = session.get(url, headers=headers)  
                        tasks.append((u, task))  
                    results = await asyncio.gather(*[t[1] for t in tasks], return_exceptions=True)  
                    for (u, _), r in zip(tasks, results):  
                        if isinstance(r, ClientConnectorError):  
                            print(f"{yellow_console}⚠ internet lost during rare check... retrying")  
                            await asyncio.sleep(5)  
                            break  
                        elif r.status == 404:  
                            print(f"{green_console}✅ Available: {u}")  
                            await send_telegram_message(u)  
                            save_username_to_file(u)  
                        else:  
                            print(f"{red_console}❌ Taken: {u}")  
        except ClientConnectorError:  
            print(f"{yellow_console}⚠ no internet at all... waiting to resume...")  
            await asyncio.sleep(5)  
  
# Runner  
async def main(username_type):  
    if username_type == 'RARE':  
        await check_rare_usernames()  
    else:  
        async with aiohttp.ClientSession() as session:  
            while True:
                try:
                    await asyncio.gather(*[create_instagram_account(session, username_type) for _ in range(10)])  
                except Exception as e:
                    print(f"{red_console}❌ Main loop error: {e}, restarting in 10 seconds...")
                    await asyncio.sleep(10)

if __name__ == "__main__":
    # Auto-select option 8 and start
    print('\033[1;34mAuto-selected: 4L (All combos: a-z, 0-9, _, .)')
    print(f'{yellow_console}🚀 Starting 24/7 checker...')
    print(f'{yellow_console}⚡ Bot will run continuously and send Telegram alerts')
    print(f'{yellow_console}🔄 Keep-alive system enabled')

    username_type = '4A'  
    
    # Start with automatic restart
    while True:
        try:
            asyncio.run(main(username_type))
        except Exception as e:
            print(f"{red_console}❌ Critical error: {e}, restarting in 30 seconds...")
            time.sleep(30)
