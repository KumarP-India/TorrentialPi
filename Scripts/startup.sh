#!/bin/bash
: <<'Metadata'
@Author: Prabhas Kumar
@Assistant: ChatGPT Plus (GPT 4), GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: startup.sh [Shell script]
Metadata


# Start Transmission Daemon
sudo systemctl start transmission-daemon

# If unsucessful put the Error status 
if [ $? -ne 0 ]; then

    echo "Transsmision Error" > "../Status_and_Logs/TorrentialPi.status"

    exit 1
fi

echo "Booting" > "../Status_and_Logs/TorrentialPi.statuss"

# start LED program
cd /home/$USER/TorrentialPi/Scripts

/usr/bin/python3 ../Programmes/StatusLady.py &

# Put No internet status untill Internet is available
echo "No Internet" > "../Status_and_Logs/TorrentialPi.status"

# Wait for an internet connection
while ! ping -c 1 8.8.8.8 >/dev/null 2>&1; do

    sleep 1
done

echo "Booting" > "../Status_and_Logs/TorrentialPi.status"

exit 0
