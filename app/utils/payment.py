# app/utils/payment.py

import base64, httpx
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def get_access_token():
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")

    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = httpx.get(auth_url, auth=(consumer_key, consumer_secret))

    if response.status_code != 200:
        print("Access token error:", response.text)
        return None

    return response.json().get("access_token")


def initiate_stk_push(phone_number: str, amount: int):
    token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = os.getenv("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY")
    callback = os.getenv("MPESA_CALLBACK_URL")

    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback,
        "AccountReference": "MultisigEscrow",
        "TransactionDesc": "Escrow payment"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = httpx.post(url, headers=headers, json=payload)
    return response.json()
