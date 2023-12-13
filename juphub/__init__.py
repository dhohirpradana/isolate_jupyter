import subprocess
import re
from flask import Flask, jsonify, request
from pb_user import user_create, user_check, user_remove
from pb_token import check_connection as pb_check_connection
from hdfs import dir_create, dir_remove, check_connection as hdfs_check_connection

def generate_token(service_name):
    # check connection
    pb_check_connection()
    hdfs_check_connection()
    
    # validate request body
    required_fields = ['email', 'password', 'firstName', 'lastName']
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Request body can not be empty."}), 400
    
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field} is required."}), 400
    
    username = service_name
    password = data['password']
    email = data['email']
    first_name = data['firstName']
    last_name = data['lastName']
    
    user_not_exists = user_check(email, service_name)
    
    if not user_not_exists:
        return jsonify({"message": f"User with email {email} or username {service_name} already exists."}), 409
    
    unused_port = subprocess.run([
        '/bin/bash',
        '-c',
        f'/home/bodhaperjuangan/isolate_jupyter/unused_port.sh'
    ], capture_output=True, text=True).stdout.strip()
    
    if unused_port == "404":
        return jsonify({"message": f"Not found unused port between 38000 and 65535."}), 400
    
    port = unused_port
    
    jupyter = subprocess.run([
        '/bin/bash',
        '-c',
        f'/home/bodhaperjuangan/isolate_jupyter/jupyter.sh {service_name} {port}'
    ], capture_output=True, text=True).stdout.strip()
    
    if jupyter == "400":
        return jsonify({"message": f"Usage: {service_name} {port}"}), 400
    elif jupyter == "409":
        return jsonify({"message": f"Service {service_name} already exists. Please use a different service name."}), 409
    elif jupyter == "406":
        return jsonify({"message": f"Port {port} already in use."}), 406

    dir_create(username)
    
    jupyter = jupyter.splitlines()[-1]
    user_create(jupyter, port, username, password, email, first_name, last_name)
    return jsonify({"token": jupyter, "port": port})

def service_remove(service_name):
    # check connection
    pb_check_connection()
    hdfs_check_connection()
    
    subprocess.run([
        '/bin/bash',
        '-c',
        f'docker stack rm --volumes {service_name}'
    ], capture_output=True, text=True).stdout.strip()
    
    dir_remove(service_name)
    user_remove(service_name)
    return jsonify({"message": f"Service {service_name} removed."})