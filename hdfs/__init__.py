import requests
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

# Replace <dir-path> with the directory path you want to create
hdfs_url = os.environ.get('HDFS_URL')

# check connection
def check_connection():
    try:
        r = requests.get(hdfs_url)
        print("Connection failed to HDFS")
    except Exception as e:
        print(str(e))
        return jsonify({"message": "Error check connection to HDFS."}), 500

def dir_create(username):
    r = requests.put(hdfs_url + f"/usersapujagad/{username}?user.name={username}&op=MKDIRS")

    if r.status_code == 200:
        print("Directory created successfully")
    else:
        print("Failed to create directory")
        print(r.text)
        
def dir_remove(username):
    r = requests.delete(hdfs_url + f"/usersapujagad/{username}?user.name={username}&op=DELETE")

    if r.status_code == 200:
        print("Directory removed successfully")
    else:
        print("Failed to remove directory")
        print(r.text)
