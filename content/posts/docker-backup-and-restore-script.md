+++
title = "Docker Volume Backup and Restore Script"
date = 2023-09-06T09:02:03+00:00
tags = []
featured = false
draft = false
feature_image = "https://images.unsplash.com/photo-1589995186011-a7b485edc4bf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDR8fGJhY2t1cHxlbnwwfHx8fDE2OTM5OTA4OTl8MA&ixlib=rb-4.0.3&q=80&w=2000"
+++

In this guide, we'll walk through a Python script that allows you to backup and restore Docker containers remotely using SSH. This script is especially useful if you need to safeguard your containers and their data. We'll break this guide into two sections: **Backup** and **Restore**.
[GitHub - Techdox/docker_backup: Easy backup solution of Docker VolumesEasy backup solution of Docker Volumes. Contribute to Techdox/docker_backup development by creating an account on GitHub.

![](https://github.githubassets.com/pinned-octocat.svg)

GitHubTechdox

![](https://opengraph.githubassets.com/12f683df4e868cc407725ab75714a03f0d2d829ef53f38a9a607b73e97b38503/Techdox/docker_backup)

](https://github.com/Techdox/docker_backup/tree/main)
### Prerequisites

Before you begin, ensure you have the following prerequisites:

- A remote server with Docker installed.
- SSH access to the remote server with the necessary credentials.
- Python and the Paramiko library installed on your local machine.

### Backup

#### Step 1: Prepare the Backup Script

Copy and paste the following Python script into a file on your local machine. Replace the placeholders in the script (e.g., `REMOTE_HOSTNAME`, `REMOTE_USERNAME`, `PRIVATE_KEY_PATH`) with your remote server's details.

```
import paramiko
import os

# Constants for SSH connection details
REMOTE_HOSTNAME = ''
REMOTE_PORT = 22  # SSH default port
REMOTE_USERNAME = ''
PRIVATE_KEY_PATH = ''

def run_remote_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def backup_container(container_name, backup_file_name, backup_path, local_destination):
    # Commands
    stop_command = f'docker stop {container_name}'
    start_command = f'docker start {container_name}'
    backup_command = (
        f'docker run --rm --volumes-from {container_name} '
        f'-v $(pwd):/backup ubuntu bash -c '
        f'"cd {backup_path} && tar cvf /backup/{backup_file_name}.tar ."'
    )

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)

        # Connect to the remote server using key-based authentication
        ssh_client.connect(REMOTE_HOSTNAME, REMOTE_PORT, REMOTE_USERNAME, pkey=private_key)

        # Execute commands
        run_remote_command(ssh_client, stop_command)
        print("Docker container stopped.")
        run_remote_command(ssh_client, backup_command)
        run_remote_command(ssh_client, start_command)
        print("Docker container started.")

        # Construct remote and local file paths
        remote_backup_file_path = os.path.join(ssh_client.exec_command('echo $HOME')[1].read().decode().strip(), f'{backup_file_name}.tar')
        local_backup_file_path = os.path.join(local_destination, f'{backup_file_name}.tar')

        # Create an SCP client from the SSH client
        scp_client = ssh_client.open_sftp()

        # Download the backup file from the remote server to the local machine
        scp_client.get(remote_backup_file_path, local_backup_file_path)
        print("Backup file downloaded successfully.")

    finally:
        # Close the SCP client and SSH connection
        scp_client.close()
        ssh_client.close()

def get_user_input():
    container_name = input("Enter the container name to backup: ")
    backup_file_name = input("Enter the backup file name: ")
    backup_path = input("Enter the backup path: ")
    local_destination = input("Enter the local destination path to save the backup file: ")

    return container_name, backup_file_name, backup_path, local_destination

def main():
    container_name, backup_file_name, backup_path, local_destination = get_user_input()
    backup_container(container_name, backup_file_name, backup_path, local_destination)

if __name__ == '__main__':
    main()`
```

Save the script with a `.py` extension, e.g., `docker_backup.py`.

#### Step 2: Run the Backup Script

Open a terminal and navigate to the directory where you saved the script. Run the script by executing:

```
python docker_backup.py`
```

The script will prompt you for the following information:

- Container name to backup.
- Backup file name. (What you want to save the file as, do not specify an extension, it is .tar by default.)
- Backup path within the container. (Path of the directory you want to backup, e.g. /var/lib/mysql/
- Local destination path to save the backup file.

Provide the requested information.

#### Step 3: Backup Execution

The script will perform the following steps:

1. Stop the Docker container temporarily.
2. Create a backup of the specified directory within the container.
3. Start the Docker container again.
4. Download the backup file to your local machine.

### Restore

#### Step 1: Prepare the Restore Script

Copy and paste the following Python script into another file on your local machine. Replace the placeholders in the script (e.g., `REMOTE_HOSTNAME`, `REMOTE_USERNAME`, `PRIVATE_KEY_PATH`) with your remote server's details.

```
import paramiko

# Constants for SSH connection details
REMOTE_HOSTNAME = ''
REMOTE_PORT = 22  # SSH default port
REMOTE_USERNAME = ''
PRIVATE_KEY_PATH = ''

def run_remote_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def main():
    # Get user input
    container_name = input("Enter the container name to restore: ")
    backup_file_name = input("Enter the backup file name: ")
    backup_path = input("Enter the backup path: ")
    backup_source = input("Enter the backup source on the remote server: ")

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)

        # Connect to the remote server using key-based authentication
        ssh_client.connect(REMOTE_HOSTNAME, REMOTE_PORT, REMOTE_USERNAME, pkey=private_key)

        # Commands
        stop_command = f'docker stop {container_name}'
        start_command = f'docker start {container_name}'
        restore_command = (
            f'docker run --rm --volumes-from {container_name} '
            f'-v {backup_source}:/backup ubuntu bash -c '
            f'"rm -rf {backup_path}/* && cd {backup_path} && tar xvf /backup/{backup_file_name}.tar"'
        )

        # Execute commands
        run_remote_command(ssh_client, stop_command)
        print("Docker container stopped.")
        run_remote_command(ssh_client, restore_command)
        run_remote_command(ssh_client, start_command)
        print("Docker container started.")

    finally:
        # Close the SSH connection
        ssh_client.close()

if __name__ == '__main__':
    main()`
```

Save the script with a `.py` extension, e.g., `docker_restore.py`.

#### Step 2: Run the Restore Script

Open a terminal and navigate to the directory where you saved the script. Run the script by executing:

```
python docker_restore.py`
```

The script will prompt you for the following information:

- Container name to restore.
- Backup file name. (The name of the backup file you wish to restore, needs to be a .tar file, do not specify the extension)
- Backup path within the container. (When you will restore the files, e.g. /var/lib/mysql/)
- Backup source on the remote server. (Where the backup file is stored, needs to be accessible by the server running the container.)

Provide the requested information.

#### Step 3: Restore Execution

The script will perform the following steps:

1. Stop the Docker container temporarily.
2. Remove the existing data in the specified directory within the container.
3. Restore data from the backup file.
4. Start the Docker container again.

{{< racknerd >}}

### Conclusion

You now have a comprehensive guide on how to use these Docker backup and restore scripts. With these scripts, you can easily safeguard your Docker containers and their data on a remote server. Make sure to schedule regular backups to ensure the safety of your valuable data.

Feel free to reach out if you encounter any issues or have further questions. Happy Docker container management!

  
[](https://www.buymeacoffee.com/techdox)
