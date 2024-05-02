#!/bin/bash
: <<'Metadata'
@Author: Prabhas Kumar
@Assistant: ChatGPT Plus (GPT 4), GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: Guardsman [Shell script]
Metadata

# Configuration
CLEANER_SCRIPT_PATH="./CleanerScript.sh"
RECOMMENDATION_FILE="../Status_and_Logs/CleanerRecommendation.list"
EMAIL_RECIPIENT="TODOEMAAIL"
DISK_PARTITION="TODODISKPART" 
SCRIPT_LOG="../Status_and_Logs/Scripts.log"

# Log script identification
echo "-----------------------------------------" >> "$SCRIPT_LOG"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Starting" >> "$SCRIPT_LOG"
echo "-----------------------------------------" >> "$SCRIPT_LOG"

# Fetch current disk usage in GB
echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Checking disk space usage." >> "$SCRIPT_LOG"

current_usage=$(df -BG $DISK_PARTITION | grep $DISK_PARTITION | awk '{print $3}' | sed 's/G//')

if [ $? -ne 0 ]; then

    > "$STATUS_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Can not calculate current disk usage" >> "$SCRIPT_LOG"

    exit 1
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Current usage: $current_usage GB" >> "$SCRIPT_LOG"

# Define thresholds in GB
threshold_critical=TODOCRITICAL  # Critical: TODOCRITICALGB used, triggers cleaner and email (critical capacity)
threshold_high=TODOHIGH       # High: TODOHIGHGB used, sends warning email (low capacity)
threshold_medium=TODOMEDM     # Medium: TODOMEDMGB used, sends informational email (50% crossed)
threshold_low=TODOLOW        # Low: TODOLOWGB used, sends informational email (considerable capacity)

# Check disk usage against thresholds and take appropriate actions
if [ "$current_usage" -ge "$threshold_critical" ]; then

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Usage exceeds critical threshold. Running CleanerScript.sh." >> "$SCRIPT_LOG"

    bash "$CLEANER_SCRIPT_PATH"

    if [ -f "$RECOMMENDATION_FILE" ]; then

        recommendations=$(cat "$RECOMMENDATION_FILE")

        echo -e "Your torrent server is critically full. Here are some recommendations to free up space:\n$recommendations" | mail -s "Alert! Torrent Server is full." "$EMAIL_RECIPIENT"

        if [ $? -ne 0 ]; then

            > "$STATUS_FILE"

            echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Failed to send Email." >> "$SCRIPT_LOG"

            exit 1
        fi

        echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsmn: Email sent with recommendations due to critical capacity (highest priority.)" >> "$SCRIPT_LOG"
    fi

    else
    
        > "$STATUS_FILE"

        echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Failed to get recommendation from CleanerScript.sh." >> "$SCRIPT_LOG"

        exit 1
    fi

elif [ "$current_usage" -ge "$threshold_high" ]; then

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Usage exceeds high threshold. Sending 80% full warning email." >> "$SCRIPT_LOG"

    echo "Your torrent server has reached 80% capacity. Consider checking and cleaning up unnecessary files." | mail -s "Warning: Torrent Server 80% full." "$EMAIL_RECIPIENT"

    if [ $? -ne 0 ]; then

        > "$STATUS_FILE"

        echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Failed to send Email." >> "$SCRIPT_LOG"

        exit 1
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Warning email sent due to low capacity (medium priority.)" >> "$SCRIPT_LOG"

elif [ "$current_usage" -ge "$threshold_medium" ]; then

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Usage exceeds medium threshold. Sending 60% full information email." >> "$SCRIPT_LOG"

    echo "Your torrent server has reached 60% capacity. It's a good time to review stored data." | mail -s "Info: Torrent Server 60% full." "$EMAIL_RECIPIENT"

    if [ $? -ne 0 ]; then

        > "$STATUS_FILE"

        echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Failed to send Email." >> "$SCRIPT_LOG"

        exit 1
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Information email sent due to crossing 50% capacity (low priority.)" >> "$SCRIPT_LOG"

elif [ "$current_usage" -ge "$threshold_low" ]; then

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Usage exceeds low threshold. Sending 50% full information email." >> "$SCRIPT_LOG"

    echo "Your torrent server has reached 50% capacity. Please be aware of the growing data." | mail -s "Info: Torrent Server 50% full." "$EMAIL_RECIPIENT"

    if [ $? -ne 0 ]; then

        > "$STATUS_FILE"

        echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Failed to send Email." >> "$SCRIPT_LOG"

        exit 1
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: Information email sent due to considrable capacity (least priority.)" >> "$SCRIPT_LOG"
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - Guardsman: completed." >> "$SCRIPT_LOG"

exit 0
