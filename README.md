# LOLDoors
LOLDoors is a Python script designed for automating the setup of reverse shells and backdoors on a target Linux system.
LOLDoors was created as a quick and dirty shell script generator for backdooring and maintaining persistence on linux machines. Just run the python script on your host and paste the output into a compromised terminal (root access works best).

## Installation
```
git clone https://github.com/Jacob-Ham/LOLDoors.git
cd LOLDoors
sudo /usr/bin/chmod u+x LOLDoors.py && /usr/bin/sudo /usr/bin/cp -p LOLDoors.py /usr/bin/LOLDoors
```

## Usage
```
LOLDoors <LHOST> <LPORT>
```
## Functionalities

- User Cronjob Reverse Shell: Creates a cronjob for a user with a reverse shell that runs every minute.
- System Cronjob Reverse Shell: Sets up a system-wide cronjob with a root-level reverse shell.
- SSH Persistence: Adds your SSH key to the authorized keys file for the user and root, allowing passwordless SSH access.
- File Privilege Escalation: Creates a binary with setuid privileges for running commands with root access.
- Python Bind Shells: Sets up multiple Python bind shells for remote connections.
- Fake Service Backdoor: Creates a fake systemd service for continuous reverse shell access.
