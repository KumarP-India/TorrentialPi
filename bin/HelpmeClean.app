#!/bin/bash
: <<'Metadata'
@Author: Prabhas Kumar
@Assistant: ChatGPT Plus (GPT 4), GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: Help me Clean [Shell script]
Metadata

LOG_FILE="./TorrentialPi/TorrentialPi/Status_and_Logs/Scripts.log"

log_message() {

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Help me Clean: $1." >> "$LOG_FILE"
}

echo "--------------------------------------------------------" >> "$LOG_FILE"
log_message "Started"
echo "--------------------------------------------------------" >> "$LOG_FILE"

echo -e "Here is last generated recommendations:\n\n"


cat "./TorrentialPi/Status_and_Logs/CleanerRecommendation.list"


# Prompt the user if they want to regenerate
read -p "Do you want to regenerate? (Y/n): " REGENERATE
REGENERATE=$(echo "$REGENERATE" | tr '[:upper:]' '[:lower:]')

if [ "$REGENERATE" = "y" ]; then

    log_message "Running CleanerScript"
    
    ./TorrentialPi/Scripts/CleanerScript.sh

    echo -e "\n\n\n"

    cat "./TorrentialPi/Status_and_Logs/CleanerRecommendation.list"

    echo -e "\nHelpmeClean Exited"

    log_message "Exiting"

else
    echo "Not regenerating. Exiting..."
    echo -e "HelpmeClean Exited"
    log_message "Exited"

fi
