import requests
import time
import schedule
import pytz
from datetime import datetime

# Define the game endpoint
endpoint = 'https://sg-hk4e-api.hoyolab.com/event/sol/sign?act_id=e202102251931481'

# Function to load cookies from cookie.txt
def load_cookies(cookie_file):
    with open(cookie_file, 'r') as file:
        cookies = file.read().strip()  # Read all cookies from the file
    return cookies

# Function to check-in using the provided cookies
def check_in(cookie):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.6',
        'connection': 'keep-alive',
        'origin': 'https://act.hoyolab.com',
        'referrer': 'https://act.hoyolab.com',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    data = {
        'lang': 'en-us',
        'act_id': 'e202102251931481'
    }

    response = requests.post(endpoint, headers=headers, json=data)
    json_resp = response.json()

    # Success and error messages
    success_codes = {
        '0': 'Successfully checked in!',
        '-5003': 'Already checked in for today'
    }
    error_codes = {
        '-100': 'Error not logged in. Invalid cookie.',
        '-10002': 'Error not found. You haven\'t played this game'
    }

    code = str(json_resp.get("retcode"))
    if code in success_codes:
        print(f"Check-in: {success_codes[code]}")
        return True  # Successful check-in
    elif code in error_codes:
        print(f"Check-in Error: {error_codes[code]}")
        return False  # Error, retry
    else:
        print(f"Check-in Error: Undocumented error.")
        return False  # Error, retry

# Load cookies from cookie.txt
cookie_file = 'cookie.txt'
cookie = load_cookies(cookie_file)

# Function to run the check-in at 3 AM Thailand time
def check_in_at_3am():
    # Print current time (in Thailand timezone)
    thailand_tz = pytz.timezone('Asia/Bangkok')
    local_time = datetime.now(thailand_tz)
    print(f"Current time (Thailand): {local_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Attempt to check in until success
    while True:
        success = check_in(cookie)
        if success:
            break  # Exit loop on success
        print("Retrying in 5 seconds...")
        time.sleep(5)  # Wait before retrying

# Schedule the task to run daily at 3 AM Thailand time
schedule.every().day.at("03:00").do(check_in_at_3am)

# Run the scheduled task 24/7
while True:
    # Run all the pending scheduled tasks
    schedule.run_pending()

    # Sleep for 1 minute before checking the schedule again
    time.sleep(60)
