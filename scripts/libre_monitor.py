import os
import sys
import hashlib
import requests
from datetime import datetime
from dotenv import load_dotenv

def get_bundle_path(filename):
    # If running as an EXE, PyInstaller stores files in a temp folder (sys._MEIPASS)
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    # Otherwise, look in the current directory
    return os.path.join(os.path.abspath("."), filename)

# Use the bundle path to load the .env
env_path = get_bundle_path(".env")
load_dotenv(env_path)

# Now your os.getenv() calls will work inside the .exe
# --- config ---
API_ENDPOINT = "https://api-eu2.libreview.io/"
LOGIN_CREDS = {
    "email": os.getenv("LIBRELINKUP_EMAIL"),
    "password": os.getenv("LIBRELINKUP_PASSWORD")
}
HEADERS_BASE = {
    'accept-encoding': 'gzip, deflate, br',
    'cache-control': 'no-cache',
    'connection': 'Keep-Alive',
    'content-type': 'application/json',
    'product': 'llu.android',
    'version': '4.16.0'
}

# --- auth ---
def login_get_auth():
    url = API_ENDPOINT + "llu/auth/login"
    response = requests.post(url, headers=HEADERS_BASE, json=LOGIN_CREDS)
    response.raise_for_status()
    user_id = response.json()["data"]["user"]["id"]
    account_id = hashlib.sha256(user_id.encode()).hexdigest()
    # print(f"account_id = {account_id}")
    token = response.json()["data"]["authTicket"]["token"]
    return "Bearer " + token, account_id

# --- get user id ---
def get_user_id(auth_token, account_id):
    url = API_ENDPOINT + "user"
    headers = HEADERS_BASE.copy()
    headers["authorization"] = auth_token
    headers["account-id"] = account_id
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["user"]["id"]

# --- trend ---
def get_trend(value):
    return {
        1: ("↓"),
        2: ("↘"),
        3: ("→"),
        4: ("↗"),
        5: ("↑")
    }.get(value, ("?"))

# --- get current glucose value ---
def get_current_value(auth_token, user_id, account_id):
    url = API_ENDPOINT + f"llu/connections/{user_id}/graph"
    headers = HEADERS_BASE.copy()
    headers["authorization"] = auth_token
    headers["account-id"] = account_id
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()["data"]["connection"]
    glucose = str(data["glucoseMeasurement"]["Value"])
    trend_value = data["glucoseMeasurement"]["TrendArrow"]
    api_timestamp_str = data["glucoseMeasurement"]["Timestamp"]

    # Convert API timestamp (from Libre) to datetime
    try:
        api_time = datetime.strptime(api_timestamp_str, '%m/%d/%Y %I:%M:%S %p')
        api_time_str = api_time.strftime('%d/%m/%Y - %H:%M')
    except ValueError:
        api_time_str = "Invalid"

    trend = get_trend(trend_value)
    print(glucose, trend, api_time_str)
    return glucose, trend, api_time_str

# --- main ---
def main():
    try:
        token, account_id = login_get_auth()
        user_id = get_user_id(token, account_id)
        get_current_value(token, user_id, account_id)
    except Exception as e:
        print(f"E {e}")

if __name__ == "__main__":
    main()


