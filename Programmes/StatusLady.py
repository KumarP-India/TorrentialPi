#!/usr/bin/env python3
'''
@Author: Prabhas Kumar
@Assistant: GitHub Copilot

@Created: April 30'24
@Updated: None

@Project: Torrential Pi Version 1
@File: StatusLady [Python 3(.12) script]
'''

from typing import Dict, Tuple
import json
import RPi.GPIO as GPIO
import time
import transmissionrpc # Lib. to fetch data from Trasnission

class LED:
    '''
An interface to Turn LEDs on/ off

Args:

    settings: [Dict] containing data from JSON file holding configration
    '''

    def __init__(self, settings: Dict[str, int]) -> None:
        '''Set up the GPIO pins'''
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(settings['GPIO Red'], GPIO.OUT)  # Red LED
        GPIO.setup(settings['GPIO Green'], GPIO.OUT)  # Green LED
        GPIO.setup(settings['GPIO Yellow'], GPIO.OUT)  # Yellow LED

    def R(self) -> None:
        '''Turn on the red LED'''
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)

    def G(self) -> None:
        '''Turn on the green LED'''
        GPIO.output(18, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)

    def Y(self) -> None:
        '''Turn on the yellow LED'''
        GPIO.output(18, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.HIGH)

    def Off(self) -> None:
        '''Turn off all LEDs'''
        GPIO.output(18, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)

    def RG(self) -> None:
        '''Turn on the red and green LEDs'''
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)

    def RY(self) -> None:
        '''Turn on the red and yellow LEDs'''
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.HIGH)

    def GY(self) -> None:
        '''Turn on the green and yellow LEDs'''
        GPIO.output(18, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)

    def RGY(self) -> None:
        '''Turn on all LEDs'''
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)

class Sex:
    '''
Helper class for Torrent Staus Updating Tasks

Args:

    settings: [Dict] containing data from JSON file holding configration
    '''

    def __init__(self, settings: Dict[str, str | int]) -> None:
        '''Sets up connection Transmission remote via transmissionrpc'''
        self.tc = transmissionrpc.Client(
            'localhost', 
            port=settings['Transmission Port'],
            user=settings['Transmission Username'],
            password=settings['Transmission Password']
            )
        
    def Check(self) -> Tuple[bool, bool]:
        '''
Tells you if Transmission is downloading, and if Transmission is seeding.

Returns:
        Tuple[bool, bool]:
            downloading: Boolean value for the question: Is Transmission downloading?
            eeding: Boolean value for the question: Is Transmission seeding?
        '''
        torrents = self.tc.get_torrents()
        downloading = any(t.status == "downloading" for t in torrents)
        seeding = any(t.status == "seeding" for t in torrents)
        return downloading, seeding
    

class Pussy:
    '''
Helper class for USB Staus Updating Tasks.

Args:

    LED: [Intialised class reference] Intialised LED class (Check doc string of LED for more information)
    
Acessable Functions:

    Error: For USB Script Error. Refer to TorrentialPi.log and TransferWoman.sh for more information
    
    Transfer: When USB Script is transfering files to USB
    
    Done: When USB Script has sucessfullt transfered as much files as it can and unmounted the device
    '''

    def __init__(self, LED:LED) -> None:
        
        self.LED = LED

    def Error(self) -> None: self.LED.RGY()

    def Transfer(self) -> None: self.LED.RY()

    def Done(self) -> None: self.LED.RG()
    

class Interface:
    '''
The class used to run everything in this script.

Args:

    statusFile: [Srting] Path to TorrentialPi.status
    
    settings: [String] JSON file holding configration
    '''

    def __init__(self, statusFile: str, settings: str) -> None:

        try:
            self.input = statusFile
            
            # load the configration from JSON file as dict
            with open(settings, 'r') as f:
                settings = json.load(f)

            self.Sex = Sex(settings)

            self.LED = LED(settings)

            self.Pussy = Pussy(self.LED)

            self.status = ''

            self._Check()

        except:

            self.status = '' # Code for something unexpected error

            self.Run()

    def Run(self) -> None:

        while True:

            self._Check()

            try:
                
                if self.status == 'Torrent': self._Torrent() # When USB device is not connected

                elif 'USB' in self.status: self._USB() # When USB device is connected

                elif self.status == 'Booting': self.LED.Off() # When Startup Script is running

                else: self._Fuck() # Function to show error steates

            except: self._Fuck() # Code to show something unexpected error


    def _Check(self) -> None:
        '''
Function to check TorrentialPi.status for current status
        '''

        with open(self.input, 'r') as f:

            self.status = f.readline().strip()

        # As we have Empty string for something unexpected error while other uses this for Script Errors - we have to change it something else
        if self.status == '': self.status = 'Script Error'
    
    def _Torrent(self) -> None:
        '''
Function handles States when USB Script is not running
        '''
        
        downloading, seeding = self.Sex.Check()

        if downloading: 

            if seeding: self.LED.GY()
            
            else: self.LED.G()

        elif seeding: self.LED.Y()

        else: self.LED.R()

        time.sleep(5) # Time given before rechecking by Run() via _Check()

    def _USB(self) -> None:
        '''
Function handles States when USB Script is running
        '''

        match self.status:
        
            case 'USB-Error': self.Pussy.Error()
            
            case 'USB-Transfer': self.Pussy.Transfer()
            
            case 'USB-Done': self.Pussy.Done()
        

        time.sleep(5) # Time given before rechecking by Run() via _Check()


    def _Fuck(self) -> None:
        '''
Function handles all Error States
        '''
        # Error on Transmission
        if 'Transsmision' in self.status:

            self.LED.Y()

            time.sleep(1)

            self.LED.Off()

            time.sleep(0.9) # Time given before rechecking by Run() via _Check(). Less than above as this is for blinking

        # No internet
        elif 'Internet' in self.status:

            self.LED.R()

            time.sleep(1)

            self.LED.Off()

            time.sleep(0.9) # Time given before rechecking by Run() via _Check(). Less than above as this is for blinking

        # Something unexpected error
        elif self.status == '':

            self.LED.RGY()

            time.sleep(1)

            self.LED.Off()

            time.sleep(0.9) # Time given before rechecking by Run() via _Check(). Less than above as this is for blinking


        # Scrips error
        else:

            self.LED.G()

            time.sleep(1)

            self.LED.Off()

            time.sleep(0.9) # Time given before rechecking by Run() via _Check(). Less than above as this is for blinking

statusFile = '../Status_and_Logs/TorrentialPi.status'
settings = '../Settings.json'

main = Interface(statusFile, settings)

main.Run()
