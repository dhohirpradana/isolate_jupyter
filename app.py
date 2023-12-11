from flask import Flask, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

from pb_user import user_create
from juphub import generate_token, service_remove

required_env_vars = ["PB_URL", "PB_LOGIN_URL", "PB_MAIL", "PB_USER_URL", "PB_PASSWORD", "HDFS_URL"]

def validate_envs():
    for env_var in required_env_vars:
        if env_var not in os.environ:
            raise EnvironmentError(
                f"Required environment variable {env_var} is not set.")

@app.route('/jupyserv/<username>', methods=['POST'])
def jupyserv_create(username):
    validate_envs()
    return generate_token(username)

@app.route('/jupyserv/<username>', methods=['DELETE'])
def jupyserv_remove(username):
    return service_remove(username)

@app.route('/test', methods=['GET'])
def test():
    return user_create()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
