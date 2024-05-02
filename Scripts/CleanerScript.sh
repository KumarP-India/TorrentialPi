#!/bin/bash
: <<'Metadata'
@Author: Prabhas Kumar
@Assistant: ChatGPT Plus (GPT 4), GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: CleanerScript [Shell script]
Metadata

# Configuration for transmission-remote
HOST='localhost'
PORT='TODOPORT'
USER='TODOUSERTRANS'
PASS='TODOPASSTRANS'

# Log and recommendation files
LOG_FILE="../Status_and_Logs/transfered.log"
STATUS_FILE="../Status_and_Logs/TorrentialPi.status"
SCRIPT_LOG="../Status_and_Logs/Scripts.log"
RECOMMENDATION_FILE="../Status_and_Logs/CleanerRecommendation.list"

# Start logging
echo "----------------------------------------" >> "$SCRIPT_LOG"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Starting CleanerScript.sh" >> "$SCRIPT_LOG"
echo "----------------------------------------" >> "$SCRIPT_LOG"

# Fetch all torrent info
echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Fetching torrent data from Transmission." >> "$SCRIPT_LOG"

torrent_list=$(transmission-remote $HOST:$PORT --auth $USER:$PASS -l | sed -e '1d;$d;s/^ *//')

if [ $? -ne 0 ]; then

    > "$STATUS_FILE"

    echo "Failed to fetch torrent list from Transmission." >> "$SCRIPT_LOG"

    exit 1
fi

# Array to store torrent data: "name|date_added|ratio|size"
declare -A torrent_info_name_date_ratio_size

# Populate torrent_info arrays with necessary data
for id in $(echo "$torrent_list" | awk '{print $1}'); do

    details=$(transmission-remote $HOST:$PORT --auth $USER:$PASS -t $id -i)

    if [ $? -ne 0 ]; then

        > "$STATUS_FILE"

        echo "Failed to fetch details for torrent ID $id from Transmission." >> "$SCRIPT_LOG"

        continue
    fi

    name=$(echo "$details" | grep "Name:" | cut -d':' -f2- | xargs)

    date_added=$(date -d "$(echo "$details" | grep "Date added:" | cut -d':' -f2- | xargs)" +%s)

    ratio=$(echo "$details" | grep "Ratio:" | cut -d':' -f2- | xargs)

    size=$(echo "$details" | grep "Total size:" | cut -d':' -f2 | awk '{print $1}')

    torrent_info_name_date_ratio_size[$id]="$name|$date_added|$ratio|$size"

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Processed torrent: $name, Size: $size MB, Ratio: $ratio, Added: $date_added" >> "$SCRIPT_LOG"
done


# Clear previous recommendation contents for new iteration
echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Clearing previous recommendations." >> "$SCRIPT_LOG"

> "$RECOMMENDATION_FILE"



# Define a function to calculate and collect torrents until reaching 20GB
collect_torrents_until_20GB() {

    local -n ids=$1
    local -n selected_ids=$2
    local total_size=0

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Collecting torrents until reaching 20GB threshold." >> "$SCRIPT_LOG"

    for id in "${ids[@]}"; do

        torrent_name=$(echo "${torrent_info_name_date_ratio_size[$id]}" | cut -d'|' -f1)
        torrent_size=$(echo "${torrent_info_name_date_ratio_size[$id]}" | cut -d'|' -f4)

        if grep -q "$torrent_name" "$LOG_FILE"; then

            total_size=$(echo "$total_size + $torrent_size" | bc)
            selected_ids+=("$id")

            echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Checked torrent: $torrent_name, Current total size: $total_size MB" >> "$SCRIPT_LOG"

            if (( $(echo "$total_size >= 20480" | bc -l) )); then

                echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Threshold reached with torrent: $torrent_name, Total size: $total_size MB" >> "$SCRIPT_LOG"

                break

            fi

        fi

    done

}

# Use the function for each condition
declare -a first_half_result
declare -a highest_ratio_result
declare -a oldest_result

# Save results and log actions
echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Saving recommendations to file." >> "$SCRIPT_LOG"

for id in "${first_half_result[@]}"; do

    recommendation_entry="${torrent_info_name_date_ratio_size[$id]}"

    echo "$recommendation_entry" >> "$RECOMMENDATION_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Saved to recommendation file: $recommendation_entry" >> "$SCRIPT_LOG"
done

for id in "${highest_ratio_result[@]}"; do

    recommendation_entry="${torrent_info_name_date_ratio_size[$id]}"

    echo "$recommendation_entry" >> "$RECOMMENDATION_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Saved to recommendation file: $recommendation_entry" >> "$SCRIPT_LOG"
done

for id in "${oldest_result[@]}"; do

    recommendation_entry="${torrent_info_name_date_ratio_size[$id]}"

    echo "$recommendation_entry" >> "$RECOMMENDATION_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: Saved to recommendation file: $recommendation_entry" >> "$SCRIPT_LOG"
done

echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleaner: CleanerScript.sh completed." >> "$SCRIPT_LOG"

exit 0
