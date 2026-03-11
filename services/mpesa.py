import requests
import base64
from datetime import datetime
import os

consumer_key = os.getenv("MPESA_CONSUMER_KEY")
consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
passkey = os.getenv("MPESA_PASSKEY")
shortcode = os.getenv("MPESA_SHORTCODE")
callback_url = os.getenv("MPESA_CALLBACK_URL")

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=(consumer_key, consumer_secret))
    return response.json()["access_token"]


def stk_push(phone, amount):
    access_token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        (shortcode + passkey + timestamp).encode()
    ).decode("utf-8")

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "TruHome",
        "TransactionDesc": "Clothes Purchase"
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    return response.json()