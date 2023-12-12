#!/bin/bash

# Check if arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <service_name> <port>"
    exit 1
fi

# Extract arguments
service_name=$1
port=$2

# Check if container/service already exists
if [ "$(docker ps -q -f name=$service_name)" ]; then
    echo "Service '$service_name' already exists. Please use a different service name."
    exit 1
fi

# Check if the port is already in use
if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
    echo "Port $port is already in use."
    exit 1
fi

# Create docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  $service_name:
    image: 103.127.97.93:5000/jupyter-spark
    deploy:
      replicas: 1
    ports:
      - "$port:8888"
    volumes:
      - jupyter$service_name:/home/jovyan/work
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - GRANT_SUDO=yes

volumes:
  jupyter$service_name:
EOF

# Deploy the stack
docker stack deploy -c docker-compose.yml $service_name

# Wait for a while for the service to start (adjust this timing according to your setup)
sleep 10

# Get the token from the logs of one of the containers
jtoken=$(docker service logs $service_name_$service_name | grep "token=" | awk -F"token=" '{print $2}' | awk '{print $1}' | head -n 1)

echo "Token for $service_name service is: $jtoken"