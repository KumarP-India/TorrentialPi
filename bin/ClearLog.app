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


# Function to display the menu and handle user's choice
confirm() {
    log_message "User selected $1 to clear."
    whiptail --yesno "Are you sure you want to clear $1?" 10 60
    return $?
}

# Display menu with three options using whiptail
options=("Universal log file (Scripts.log)" "Transfer History (transfered.log)")
choice=$(whiptail --title "ClearLog.app" --menu "Choose a log file to empty." 15 60 3 "${options[@]}" 3>&1 1>&2 2>&3)

case $choice in
    "Universal log file (Scripts.log)")
        
        if confirm "Scripts.log"; then

            log_message "User confirmed clearing of Scripts.log"

            > "./TorrentialPi/TorrentialPi/Status_and_Logs/Scripts.log"

            log_message "Cleared Scripts.log"

        else

            log_message "User declined clearing of Scripts.log"

        fi

        ;;
    "Transfer History (transfered.log)")
        
        if confirm "transfered.log"; then

            log_message "User confirmed clearing of transfered.log"

            > "./TorrentialPi/TorrentialPi/Status_and_Logs/transfered.log"

            log_message "Cleared transfered.log"

        else

            log_message "User declined clearing of transfered.log"

        fi

        ;;
    *)
        echo "Invalid option"
        ;;
esac