import gspread
from google.oauth2.service_account import Credentials
import os
import requests
from dotenv import load_dotenv

load_dotenv()
# url = os.getenv('google_sheet_webapp_url')
url = "https://script.google.com/macros/s/AKfycbw_N1HbmGf6TGaMdJl6kOwUDC5itHEAO1vhi2Gm0qPOBUBCPXaN8t4PPPvYYgvjCxBl/exec"
url = "https://script.google.com/macros/s/AKfycbw-IEbvmCiKQx3WYtpEjHhnNoi4NpyWnsUZztlSgQgce9oXe7snEvj2nXRjwX2Hm-I0/exec"
payload = {}
res = requests.post(url, json=payload)
print(res.text)
