#!/bin/bash

# Check if a username argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

# Assign the first argument to the variable 'username'
username="$1"

# Execute the commands
sudo docker exec -it $(docker ps --format '{{.Names}}' | grep 'hdfs-hive_namenode') groupadd $username
sudo docker exec -it $(docker ps --format '{{.Names}}' | grep 'hdfs-hive_namenode') useradd -g $username $username
sudo docker exec -it $(docker ps --format '{{.Names}}' | grep 'hdfs-hive_namenode') hdfs dfs -mkdir /usersapujagad/$username
sudo docker exec -it $(docker ps --format '{{.Names}}' | grep 'hdfs-hive_namenode') hdfs dfs -chown $username:$username /usersapujagad/$username
sudo docker exec -it $(docker ps --format '{{.Names}}' | grep 'hdfs-hive_namenode') hdfs dfs -chmod 755 /usersapujagad/$username
