#!/bin/bash
: <<'Metadata'
@Author: Prabhas Kumar
@Assistant: ChatGPT Plus (GPT 4), GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: TransferWoman [Shell script]
Metadata

# Configuration
MOUNT_POINT="TODOMOUNT"
DESKTOP_DIR="TODODOWNFOLDERTRANS"
LOG_FILE="../Status_and_Logs/Scripts.log"
USB_LOG="../Status_and_Logs/transfered.log"
TRANS_REMOTE="transmission-remote localhost --auth TODOTRANSUSER:TODOTRANSPASS"
DEVICE="/dev/sda1"
STATUS_FILE="../Status_and_Logs/TorrentialPi.status"

echo "--------------------------------------------------" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: initiated." >> "$LOG_FILE"
echo "--------------------------------------------------" >> "$LOG_FILE"

# Function to format and mount USB drive
format_and_mount_usb() {

    echo "USB-Transfer" > "$STATUS_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Formatting USB device $DEVICE to ExFAT." >> "$LOG_FILE"

    sudo mkfs.exfat $DEVICE

    if [ $? -ne 0 ]; then

        echo "USB-Error" > "$STATUS_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Failed to Format the Disk." >> "$LOG_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: exiting with error." >> "$LOG_FILE"

        exit 1
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: USB device formatted to ExFAT." >> "$LOG_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Mounting USB device to $MOUNT_POINT." >> "$LOG_FILE"

    mkdir -p $MOUNT_POINT
    mount -t exfat $DEVICE $MOUNT_POINT

    if [ $? -ne 0 ]; then

        echo "USB-Error" > "$STATUS_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Failed to mount drive." >> "$LOG_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: exiting with error." >> "$LOG_FILE"

        exit 1
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: USB device mounted at $MOUNT_POINT." >> "$LOG_FILE"
}


# Function to fetch torrents info, sort, and copy files
transfer_files() {

    # Get torrent info
    torrents=$($TRANS_REMOTE -l | sed -e '1d;$d;s/^ *//' | awk '{print $1}')

    if [ $? -ne 0 ]; then

        echo "USB-Error" > "$STATUS_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Failed to fetch torrent list from Transmission." >> "$LOG_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: exiting with error." >> "$LOG_FILE"

        exit 1
    fi

    declare -A torrent_info

    # Gather details
    for id in $torrents; do

        info=$($TRANS_REMOTE -t $id -i)

        if [ $? -ne 0 ]; then

            echo "USB-Error" > "$STATUS_FILE"
            echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Failed to fetch details for torrent ID $id from Transmission." >> "$LOG_FILE"

            continue
        fi

        name=$(echo "$info" | grep "Name:" | cut -d':' -f2- | xargs)

        date_added=$(date -d "$(echo "$info" | grep "Date added:" | cut -d':' -f2- | xargs)" +%s)

        size=$(echo "$info" | grep "Total size:" | cut -d':' -f2 | awk '{print $1}')

        path=$(echo "$info" | grep "Location:" | cut -d':' -f2- | xargs)

        file_path="$path/$name"

        torrent_info[$date_added]="$file_path $size"
    done

    # Sort by date added descending and copy files
    total_copied=0

    for key in $(echo ${!torrent_info[@]} | tr ' ' '\n' | sort -r); do

        file=${torrent_info[$key]}

        file_path=$(echo "$file" | awk '{print $1}')

        file_size=$(echo "$file" | awk '{print $2}' | sed 's/MB//')

        if [[ "$file_path" == $DESKTOP_DIR/* ]] && ! grep -q "$(basename "$file_path")" "$USB_LOG"; then

            cp "$file_path" "$MOUNT_POINT/"

            if [ $? -eq 0 ]; then

                echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Transferred file $(basename "$file_path") to USB." >> "$LOG_FILE"
                echo "$(basename "$file_path")" >> "$USB_LOG"

                total_copied=$((total_copied + file_size))

            else
                echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Failed to copy $(basename "$file_path") to USB." >> "$LOG_FILE"
            fi

        fi

    done

    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Total size of files transferred: $total_copied MB." >> "$LOG_FILE"
}


# Function to unmount USB
unmount_usb() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Unmounting USB device from $MOUNT_POINT." >> "$LOG_FILE"

    umount $MOUNT_POINT
    
    if [ $? -ne 0 ]; then
        echo "USB-Error" > "$STATUS_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: Failed to unmount." >> "$LOG_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: exiting with error." >> "$LOG_FILE"
    
        exit 1
    fi
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: USB device unmounted." >> "$LOG_FILE"

}


# Execute functions
format_and_mount_usb
transfer_files
unmount_usb

echo "USB-Done" > "$STATUS_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Transfer Woman: completed." >> "$LOG_FILE"
exit 0
