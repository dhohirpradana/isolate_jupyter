import requests
import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

pb_login_url = os.environ.get('PB_LOGIN_URL')
pb_mail = os.environ.get('PB_MAIL')
pb_password = os.environ.get('PB_PASSWORD')

# check connection
def check_connection():
    try:
        r = requests.get(pb_login_url)
        print("Connection success to PB")
    except Exception as e:
        print(str(e))
        return jsonify({"message": "Error check connection to PB."}), 500

def token_get():
    # lastRun
    try:
        r = requests.post(pb_login_url,
                          json={
                              "identity": pb_mail,
                              "password": pb_password
                          }
                          )

        r.raise_for_status()
        data = r.json()
        token = data["token"]
        print(token)
        return token
    except Exception as e:
        print(str(e))
        return jsonify({"message": "Error get token."}), 400
