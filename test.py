import subprocess

username = "test"
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

