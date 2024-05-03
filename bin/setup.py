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
    # Load the settings from the JSON file
    with open(settings_path, 'r') as file:
        settings = json.load(file)

    # Define the path to the file that needs to be modified
    file_path = './torentialpi.service'

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

def TransmissionSettings(settings_path: str):
    '''
Update the transmission settings based on the JSON file
    '''

    TransmissionSettingsFile = '/etc/transmission-daemon/settings.json'

     # Load the settings from the JSON file
    with open(settings_path, 'r') as file:
        settings = json.load(file)


    # Load the transmission settings from the file
    with open(TransmissionSettingsFile, 'r') as file:

        transmission_settings = json.load(file)

    # Update the transmission settings based on the JSON file
    for key, value in settings.items():
        if key in transmission_settings:
            transmission_settings[key] = value

    # One time Transmission Settings Update
    transmission_settings["peer-id-ttl-hours"] = 4
    transmission_settings["start-added-torrents"] = "true"
    transmission_settings["trash-original-torrent-files"] = "true"

    # Save the updated transmission settings back to the file
    with open(TransmissionSettingsFile, 'w') as file:

        json.dump(transmission_settings, file, indent=4)

    print("Transmission settings updated successfully.")

    # Define the path to the file that needs to be modified
    file_path = '/etc/init.d/transmission-daemon'

    # Define the strings to search for and their replacements based on the JSON file
    search_replace = {
        'USER': settings['Username']
    }

    # Use sed command with sudo to find and replace the strings in the file
    try:
        for search, replace in search_replace.items():
            subprocess.run(['sudo', 'sed', '-i', f's/{search}/{replace}/g', file_path], check=True)
        print("Transmission Username to us updated successfully: 50%")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred for Transmission Username to us updating [50%]: {e}")

    # Define the path to the file that needs to be modified
    file_path = '/etc/systemd/system/multi-user.target.wants/transmission-daemon.service'

    # Define the strings to search for and their replacements based on the JSON file
    search_replace = {
        'USER': settings['Username']
    }

    # Use sed command with sudo to find and replace the strings in the file
    try:
        for search, replace in search_replace.items():
            subprocess.run(['sudo', 'sed', '-i', f's/{search}/{replace}/g', file_path], check=True)
        print("Transmission Username to us updated successfully: 50%")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred for Transmission Username updating [other 50%]: {e}")

def CleanerUpdate(settings_path: str):
    '''
Update the service file with the username and user group from the JSON file.
    '''
    # Load the settings from the JSON file
    with open(settings_path, 'r') as file:
        settings = json.load(file)

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


def TransferUpdate(settings_path: str):
    '''
Update the service file with the username and user group from the JSON file.
    '''
    # Load the settings from the JSON file
    with open(settings_path, 'r') as file:
        settings = json.load(file)

    # Define the path to the file that needs to be modified
    file_path = './Scripts/TransferWoman.sh'

    # Define the strings to search for and their replacements based on the JSON file
    search_replace = {
        'TODOUSERTRANS': settings['Transmission Username'],
        'TODOPASSTRANS': settings['Transmission Password'],
        'TODOMOUNT': settings['USB Storage Device Mount location'],
        'TODODOWNFOLDERTRANS': settings['download-dir']
    }

    # Use sed command with sudo to find and replace the strings in the file
    try:
        for search, replace in search_replace.items():
            subprocess.run(['sudo', 'sed', '-i', f's/{search}/{replace}/g', file_path], check=True)
        print("TransferWoman File updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred for TransferWoman File updating: {e}")



if __name__ == '__main__':

    settings_path = './Settings.json'

    AutoStartupServiceFile(settings_path)

    TransmissionSettings(settings_path)

    CleanerUpdate(settings_path)

    TransferUpdate(settings_path)