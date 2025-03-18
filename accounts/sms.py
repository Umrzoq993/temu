import requests
import time
import hashlib

USERNAME = "saraystore"
SECRET_KEY = "8bf06c1ead5f61092685e659e400643f"


def generate_token(username, secret_key, utime):
    access_string = f"TransmitSMS {username} {secret_key} {utime}"
    return hashlib.md5(access_string.encode()).hexdigest()


def transmit_sms(sms, sms_id, phone):
    # Remove the leading '+' if present
    if phone.startswith("+"):
        phone = phone[1:]

    url = "https://routee.sayqal.uz/sms/TransmitSMS"
    utime = int(time.time())
    token = generate_token(USERNAME, SECRET_KEY, utime)
    headers = {
        "Content-Type": "application/json",
        "X-Access-Token": token
    }
    payload = {
        "utime": utime,
        "username": USERNAME,
        "service": {"service": 2},
        "message": {
            "smsid": sms_id,
            "phone": phone,
            "text": sms
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return {"status": True, "response": response.json()}
    else:
        return {"status": False, "response": response.json()}
