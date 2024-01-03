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

# Function to check if jtoken is empty
is_jtoken_empty() {
    [ -z "$jtoken" ]
}

wait_for_jtoken() {
    local timeout=30  # Maximum wait time in seconds
    local interval=1   # Interval to check in seconds
    local waited=0

    while is_jtoken_empty && [ $waited -lt $timeout ]; do
        sleep $interval
        # jtoken=$(docker logs "$service_name" | grep "token=" | awk -F"token=" '{print $2}' | awk '{print $1}' | head -n 1)
        jtoken=$(docker service logs ${service_name}_${service_name} 2>&1 | grep "token=" | awk -F"=" '{print $NF}' | tail -n 1)
        waited=$((waited + interval))
    done
}

# Create docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  $service_name:
    image: dhohirp/pyspark-jupyter
    deploy:
      replicas: 1
    ports:
      - "$port:8888"
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - GRANT_SUDO=yes
EOF

# Deploy the stack
docker stack deploy -c docker-compose.yml $service_name

# Wait for jtoken to be available
wait_for_jtoken

echo "$jtoken"
