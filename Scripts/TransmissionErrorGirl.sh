#!/bin/bash
: <<'Metadata'
@Author: Prabhas Kumar
@Assistant: ChatGPT Plus (GPT 4), GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: TransmissionErrorGirl [Shell script]
Metadata

# Log file location
LOG_FILE="../Status_and_Logs/Scripts.log"
REBOOTED="../Status_and_Logs/TorrentialPi.bootlog"

# Function to log messages
log_message() {

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transmission Error Girl: $1." >> "$LOG_FILE"
}

# Function to check Transmission for errors
check_transmission_errors() {

    # Check for active torrents with errors
    mapfile -t torrents_with_errors < <(transmission-remote -l | grep -E 'Error|Stopped' | awk '{print $1}')

    if [ ${#torrents_with_errors[@]} -ne 0 ]; then
        log_message "Critical errors found in Transmission torrents."

        return 1

    elif [ $? -ne 0 ]; then
        # If transmission-remote exits with a non-zero status, log an error message
        log_message "transmission-remote command failed with an error code."

        return 2
        
    else
        return 0
    fi
}

# Main execution block

echo "--------------------------------------------------------" >> "$LOG_FILE"
log_message "Started"
echo "--------------------------------------------------------" >> "$LOG_FILE"

if check_transmission_errors; then

    # Critical error found
    if [ -s "$REBOOTED" ]; then
        log_message "System already rEBOOTED, skipping reboot."

        > "$REBOOTED"
        > "../Status_and_Logs/TorrentialPi.status"
        
        exit 1
    
    else
        log_message "Rebooting system due to critical Transmission errors."
    
        echo "REBOOTED" > "$REBOOTED"
    
        sudo reboot
    
    fi

fi

exit 0
