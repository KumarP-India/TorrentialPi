#!/usr/bin/env python3
'''
@Author: Prabhas Kumar
@Assistant: GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: setup [Python 3(.12) script]
'''

import subprocess
import json


def AutoStartupServiceFile(settings_path: str):
    '''
Update the service file with the username and user group from the JSON file.
    '''
    print("\n\nStarting to update Auto startup Service File.")
    # Load the settings from the JSON file
    try:
        with open(settings_path, 'r') as file:
            settings = json.load(file)

            print("Settings.json file loaded successfully.")

    except:

        print("Error: Settings.json file not found.")

    # Define the path to the file that needs to be modified
    file_path = './bin/torrentialpi.service'

    # Define the strings to search for and their replacements based on the JSON file
    search_replace = {
        'TODOUSER': settings['Username'],
        'TODOGROUP': settings['User Group'],
    }

    # Use sed command with sudo to find and replace the strings in the file
    try:
        for search, replace in search_replace.items():
            subprocess.run(['sudo', 'sed', '-i', f's/{search}/{replace}/g', file_path], check=True)
        print("Auto startup Service File updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred for Auto startup Service File updating: {e}")

    print("\n\nExiting Auto startup Service File Update.")

def TransmissionSettings(settings_path: str):
    '''
Update the transmission settings based on the JSON file
    '''

    print("\n\nStarting Transmission Settings Update.")

    TransmissionSettingsFile = '/etc/transmission-daemon/settings.json'

     # Load the settings from the JSON file
    try:
        with open(settings_path, 'r') as file:
            settings = json.load(file)
            print("Settings.json file loaded successfully.")

    except:

        print("Error: Settings.json file not found.")

    # Load the transmission settings from the file
    try:
        with open(TransmissionSettingsFile, 'r') as file:

            transmission_settings = json.load(file)
            print("Transmission settings loaded successfully.")

    except:

        print("Error: Transmission settings file not found.")

    # Update the transmission settings based on the JSON file
    for key, value in settings.items():
        if key in transmission_settings:
            transmission_settings[key] = value

    # One time Transmission Settings Update
    transmission_settings["peer-id-ttl-hours"] = 4
    transmission_settings["start-added-torrents"] = "true"
    transmission_settings["trash-original-torrent-files"] = "true"

    # Save the updated transmission settings back to the file
    try:
        with open(TransmissionSettingsFile, 'w') as file:

            json.dump(transmission_settings, file, indent=4)

            print("Transmission settings updated successfully.")
            
    except Exception as e:

        print(f"Error: Transmission settings updating created: {e}.")


    override_dir = '/etc/systemd/system/transmission-daemon.service.d/'
    override_file = 'override.conf'
    
    # Ensure the override directory exists
    subprocess.run(['sudo', 'mkdir', '-p', override_dir], check=True)
    
    # Define the content to be written to the override file
    content = f"[Service]\nUser={settings['Username']}\n"
    
    # Write the content to the override file
    with open(f"{override_dir}{override_file}", 'w') as file:
        file.write(content)
    
    # Reload systemd to apply changes
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
    subprocess.run(['sudo', 'systemctl', 'restart', 'transmission-daemon'], check=True)
    print("Transmission daemon user updated successfully.")

def CleanerUpdate(settings_path: str):
    '''
Update the service file with the username and user group from the JSON file.
    '''
    print("\n\nStarting CleanerScript File Update.")

    # Load the settings from the JSON file
    try:
        with open(settings_path, 'r') as file:
            settings = json.load(file)

            print("Settings.json file loaded successfully.")

    except:

        print("Error: Settings.json file not found.")

    # Define the path to the file that needs to be modified
    file_path = './Scripts/CleanerScript.sh'

    # Define the strings to search for and their replacements based on the JSON file
    search_replace = {
        'TODOPORT': settings['Transmission Port'],
        'TODOUSERTRANS': settings['Transmission Username'],
        'TODOPASSTRANS': settings['Transmission Password']
    }

    # Use sed command with sudo to find and replace the strings in the file
    try:
        for search, replace in search_replace.items():
            subprocess.run(['sudo', 'sed', '-i', f's/{search}/{replace}/g', file_path], check=True)
        print("CleanerScript File updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred for CleanerScript File updating: {e}")

    print("\n\nExiting CleanerScript File Update.")

def TransferUpdate(settings_path: str):
    '''
    Update the service file with the username and user group from the JSON file.
    '''
    print("\n\nStarting TransferWoman File Update.")
    # Load the settings from the JSON file
    try:
        with open(settings_path, 'r') as file:
            settings = json.load(file)
            print("Settings.json file loaded successfully.")
    except FileNotFoundError:
        print("Error: Settings.json file not found.")
        return

    # Define the path to the file that needs to be modified
    file_path = './Scripts/TransferWoman.sh'

    # Define the strings to search for and their replacements based on the JSON file
    search_replace = {
        'TODOUSERTRANS': settings.get('Transmission Username', ''),
        'TODOPASSTRANS': settings.get('Transmission Password', ''),
        'TODOMOUNT': settings.get('USB Storage Device Mount location', ''),
        'TODODOWNFOLDERTRANS': settings.get('download-dir', '')
    }

    # Read the content of the file
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return

    # Perform replacements directly in Python
    for search, replace in search_replace.items():
        file_content = file_content.replace(search, replace)

    # Write the updated content back to the file
    try:
        with open(file_path, 'w') as f:
            f.write(file_content)
        print("TransferWoman File updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating TransferWoman File: {e}")

    print("\n\nExiting TransferWoman File Update.")

if __name__ == '__main__':

    settings_path = './Settings.json'

    AutoStartupServiceFile(settings_path)

    TransmissionSettings(settings_path)

    CleanerUpdate(settings_path)

    TransferUpdate(settings_path)