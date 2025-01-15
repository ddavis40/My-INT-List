import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables. Ensure it's set in your .env file.")

gameName = "plat dog"
tagLine = "NA1"
URL = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": f"{API_KEY}"
}
t = "add"
response = requests.get(URL, headers=headers)
data = response.json()
puuid = data["puuid"]

URL1 = f"https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
gameparticipants = requests.get(URL1, headers=headers)
data = gameparticipants.json()
participants = data["participants"]


