import requests
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
import subprocess

load_dotenv()

hdfs_url = os.environ.get('HDFS_URL')

# check connection
def check_connection():
    print("hdfs connecting...")
    #try:
    #    r = requests.get(hdfs_url)
    #    print("hdfs conn success")
    #    return True
    #except Exception as e:
    #    print(str(e))
    #    print("hdfs conn failed")
    #    return False
    return True

def dir_create(username):
    print("dir_create")
    container_name_or_id = "$(docker ps --format '{{.Names}}' | grep 'hdfs-hive_namenode')"
    bash_command = f"docker exec -it {container_name_or_id} groupadd {username}; \
    docker exec -it {container_name_or_id} useradd -g {username} {username}; \
    docker exec -it {container_name_or_id} hdfs dfs -mkdir -p /usersapujagad/{username}; \
    docker exec -it {container_name_or_id} hdfs dfs -chown {username}:{username} /usersapujagad/{username}; \
    docker exec -it {container_name_or_id} hdfs dfs -chmod 755 /usersapujagad/{username}"
    
    command = f"{bash_command}"
    try:
        subprocess.run(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        
def dir_remove(username):
    container_name_or_id = "$(docker ps --format '{{.Names}}' | grep 'hdfs-hive_namenode')"
    bash_command = f"docker stack rm {username}; \
    docker exec -it {container_name_or_id} hdfs dfs -rm -r /usersapujagad/{username}; \
    docker exec -it {container_name_or_id} userdel {username}; \
    docker exec -it {container_name_or_id} groupdel {username};"
 
    
    command = f"{bash_command}"
    try:
        subprocess.run(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")