import os
import requests
from flask import Flask, request, jsonify

from pb_token import token_get

pb_user_url = os.environ.get('PB_USER_URL')

def user_create(j_token, j_port, username, password, email):
    pb_token = token_get()
    try:
        r = requests.post(pb_user_url,
                        json={
                            "email": "yusuf@gmail.com",
                            "password": "2wsx1qaz",
                            "username": "yusuf",
                            "passwordConfirm": "2wsx1qaz",
                            "role": "authenticated",
                            "jToken": "",
                            "jPort": ""
                        },
                        headers={
                            "Authorization": "Bearer " + pb_token
                        }
        )
        r.raise_for_status()
        data = r.json()
        status_code = r.status_code
        return jsonify({"message": "User created."}), status_code
    except Exception as e:
        status_code = r.status_code
        print(str(e))
        return jsonify({"message": "Error create user."}), status_code
    
# check if user already exists
def user_check(email, username):
    pb_token = token_get()
    try:
        r = requests.get(pb_user_url, headers={"Authorization": "Bearer " + pb_token})
        r.raise_for_status()
        data = r.json()
        users = data["items"]
        
        print(users)
        
        # check if user not exists
        for user in users:
            if user["email"] == email or user["username"] == username:
                return False
        return True
    except Exception as e:
        print('An exception occurred')
        return jsonify({"message": "Error check user."}), 400