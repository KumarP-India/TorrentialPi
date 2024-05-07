- [x] Verify id ~ is where Github file be saved 
- [x] Change GitHub link
- [x] Change Github folder name if it is diffrent
- [x] DeveloperApp.py
- [x] Settings.json
- [x] DISK_PARTITION="/dev/root"  # TODO (Autostart?)
- [ ] TODO: 1

I assume you have flashed your SD card with the latest Raspbian OS. Now, insert your SD card into your Pi, and connect your monitor, keyboard & mouse to your Pi.

You should by default already be logged in. But if not use default credentials. At the time of writing it was:

```

Username: pi

Password: raspberry

```

Once logged in fire up the terminal as we would do everything from the terminal only. 

> Don't worry about opening this page in Pi to copy-paste as I'm gonna first set up SSH so that you can have Pi Terminal on your PC which won't be slowed when you open browser tabs.

## SSH

Run this command to get into Pi Settings GUI:

```bash
sudo raspi-config
```

Navigate: `Interfacing Options` --> `SSH` --> `<Yes>` --> `<Finish>`

> For newbies, you navigate with arrows, to jump to `<..>` use tabs, and to select use Enter/Return

You know what, while you are here go through these settings 'cause why not? For newbies, Rraspbian Settings is this only. Yes, we have GUI in Application Drawer but that opens this only.

Here is a thing, if you are gonna have a Pi server you probably already have a Router in your house/office. And since our Server is designed to be fully isolated and protected - you would want to keep it close to one of your routers/extenders. And if you are gonna go to this trouble why not use ethernet? 

Anyway, my point is that if you have a Router then you should assign this Pi a static IP. 

Your router creates a network of all devices connected to it. It takes everyone's requests and sends them one by one. So the ID (that is IP) that is given to you is for the router while the router's IP is sent to the Internet. This is by the way how we managed to not run out of IPs. 

Now, the router assigns one of the non-used IPs in the range it is advised to assign. So let's assume the Router assigned your pi of IP: `192.168.1.10` but your Pi lost power. Before you restart Pi, another device connected to your router and as `192.168.1.10` was not being used that device got `192.168.1.10` while your pi got something different. This is normal but for us, especially when using SSH where `username@devicename` is not findable, we would wanna know the Pi and finding it via the Router Page or via connecting to the monitor is not ideal. So the other solution is to just tell your Router to assign your device a reserved IP only. This way no matter whether your Pi is on or off Router will never assign that IP to anyone other than your Pi. This is called static IP and look for a guide online for your specific Router to do it.

Few more information, you would need an ID for your device that the router uses - `mac address`. Run this and look for something that looks like this (% means either number or alphabet): `%%:%%:%%:%%:%%:%%` (example {not mine}: `dc:a6:32:4a:fc:68`)

```bash
ifconfig
```

Once you have the IP (say: `192.168.1.100') of your Pi, fire up the terminal on Mac (for Windows use the internet on how to connect to SSH) and run:

```bash
ssh pi@192.168.1.100
```

As this would be your first time connecting it so your terminal will warn you about this:

```

The authenticity of host '192.168.1.100 (192.168.1.100)' can't be established.

ED25519 key fingerprint is SHA256:<Hash value>.

This key is not known by any other names.

Are you sure you want to continue connecting (yes/no/[fingerprint])?

```

If it is your first time connecting to SSH on this SD card then type `yes` else check why you have a new Hash fingerprint.

You will be asked for a Password for user `pi`. And then you are in.

## Removable of craps

We will remove some apps that are useless for us.

```bash
dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n -r | head -n 20
```

See (https://www.tomshardware.com/how-to/save-space-raspberry-pi-os) to understand the above command.

Next, I want you to search for each item in the list and know their use. If they are not required then we delete them. Here is the list of items that I deleted from the list:

```bash

sudo apt-get purge chromium-browser* pocketsphinx*

sudo apt-get remove --purge libreoffice* wolfram-engine

sudo apt-get remove --purge wolfram-engine sonic-pi

sudo apt-get remove --purge vlc

sudo apt-get clean

sudo apt-get autoremove

```

Note I also listed a few quite common heavy items from my past experiences of which many of which were not installed. So I recommend you do the research too, use the list and use the above command too. The last 2 lines clear the cache and delete any unused packages.

## Installation

Next, we need all of the packages and files. [other than GitHub Files, that's next section]

First, let's update the Pi.

```bash
sudo apt update && sudo apt upgrade
```

Next, let's install all the requirements.

```bash

sudo apt install python3-rpi.gpio

sudo apt install transmission-daemon transmission-cli

sudo apt install exfat-fuse exfatprogs

```

Finally, here we need to install one Python library.

```bash
pip install transmissionrpc
```

If your Pi doesn't let you use `pip` for installation because it is maintained by system then you can use `apt`

The error message will look like this:

```
server@pi:~ $ pip install transmissionrpc 
error: externally-managed-environment 

× This environment is externally managed 
╰─> To install Python packages system-wide, try apt install 
python3-xyz, where xyz is the package you are trying to 
install. 

If you wish to install a non-Debian-packaged Python package, create a virtual environment using python3 -m venv path/to/venv. Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make sure you have python3-full installed. 

For more information visit http://rptl.io/venv 

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages. hint: See PEP 668 for the detailed specification.
```

And this will be the fix:

```bash
sudo apt install python3-transmissionrpc
```

> It might be a good time to reboot both you and your Pi. `sudo reboot` (works from SSH too)



Now let's clean up

```bash

sudo apt-get clean 

sudo apt-get autoremove

```




## Installing Scripts and Initial Setup

First of all, we need to stop the Transmission running in the background in order to change settings and upload our scripts 

```bash
sudo systemctl stop transmission-daemon
```

Let's get my files from Github:

```bash

cd ~ 

git clone https://github.com/KumarP-India/TorrentialPi.git

```

Now we have a folder named `TorrentialPi` and this is where our files will live (except the ones that OS expects somewhere to be)

Now we go into the folder

```bash
cd ~/TorrentialPi/
```

Now we need to change a few settings. Please open `settings.json` and edit everything you want or have to. In case of confusion consult AI and/or the internet. I've planned to add this setting changing and various other stuff to GUI in `DeveloperApp` in future.

```bash
nano Settings.json
```

## Setting the system files

First, navigate inside the GitHub folder as everything is there and we will work from there. Also, make sure you're in the GitHub folder after every reboot or when no file found error happens - I won't keep reminding you.

```bash
cd ~/TorrentialPi/
```

Before we start setting up we need to make sure `sudo` doesn't require a `password` else our script won't be able to run.

To do so we open the `sudo` editor by:

```bash
sudo visudo
```

Find the line that reads `root ALL=(ALL) ALL` and add a similar line for your user, replacing `username` with your actual username. 

```bash

<username> ALL=(ALL) NOPASSWD: ALL

```

If you're using the default pi user, it will look like this:

```bash
pi ALL=(ALL) NOPASSWD: ALL
```

Now run my `setup.py` at `./bin` and it will edit the Usernames, groups, and other similar variables in the system file where reading from `Settigns.json` is not feasible & will move it to their expected location.

```bash

chmod +x ./bin/setup.py

/usr/bin/python3 ./bin/setup.py

```

Now we set up our script that needs to be running on boot. We will use Systemmd.

```bash
sudo mv ./bin/torrentialpi.service /etc/systemd/system/torrentialpi.service
```

Now we make sure all scripts are executable by setting their permission.

```bash

chmod +x ./Programmes/StatusLady.py

chmod +x ./bin/ClearLog.app

chmod +x ./bin/HelpmeClean.app

chmod +x ./bin/HelpmeClean.app

chmod +x ./bin/torrentialpi.service

chmod +x /home/$USER/TorrentialPi/Scripts/startup.sh

chmod +x /home/$USER/TorrentialPi/Scripts/CleanerScript.sh

sudo systemctl daemon-reload

sudo chown -R $USER:$USER /etc/transmission-daemon

sudo mkdir -p /home/$USER/.config/transmission-daemon/

sudo ln -s /etc/transmission-daemon/settings.json /home/$USER/.config/transmission-daemon/

sudo chown -R $USER:$USER /home/$USER/.config/transmission-daemon/

chmod +x /home/$USER/TorrentialPi/Scripts/TransferWoman.sh

chmod +x /home/$USER/TorrentialPi/Scripts/TransmissionErrorGirl.sh

```

## Final setup

Now we tell the system about our scripts and when to execute them.

First, we tell systemmd about our `.servcie` file that executes our custom startup script.

To do this we first make sure the NetworkManager is set to be active before our script is run because our script waits for the internet before exiting it.

```bash

sudo systemctl enable NetworkManager-wait-online.service

```

Now reload it and enable our script

```bash

sudo systemctl daemon-reload

sudo systemctl enable torrentialpi.service

```

Now, start the `torrentialpi.service`

```bash

sudo systemctl start torrentialpi.service

```

Verify

```bash

sudo systemctl status torrentialpi.service

```

> TODo


The second one is Transmission Error checking file: `TransmissionErrorGirl.sh`

We use cron to run this periodically. 

Let's get the path to it. Run the following and copy the output of the second line (use the mouse to copy as `ctrl + C` or `cmd + C` is for stopping not coping)

```bash

cd ~/TorrentialPi/Scripts

echo "$(pwd)/TransmissionErrorGirl.sh"

cd ~/TorrentialPi

```

Open the cron editor.

```bash

crontab -e

```

now add this:

```bash

add : 0 * * * * <what you copied/ path to your TransmissionErrorGirl.sh>

```

> Don't put `<>`



Third is  USB Transfer Automation Script. 

We use `udev` for this so open it on the editor (`nano`)

Get the path:

Run the following and copy the output of the second line (use the mouse to copy as `ctrl + C` or `cmd + C` is for stopping not coping)

```bash

cd ~~/TorrentialPi/Scripts

echo "$(pwd)/TransferWoman.sh"

cd ~/TorrentialPi

```

Open it:

```bash

sudo nano /etc/udev/rules.d/100-usb-autotransfer.rules

```

Add this:

```bash

ACTION=="add", SUBSYSTEM=="block", ENV{ID_FS_TYPE}=="exfat|vfat|ntfs", RUN+="<what you copied/ path to your TransferWoman.sh>"

```

> Don't put `<>`

Now make `udev` know and trigger it.

```bash

sudo udevadm control --reload-rules

sudo udevadm trigger

```


Next move there 2 files (their details givin in [After Setup](#After Setup)

```bash
mv ./bin/ClearLog.app ~/ClearLog.app

mv ./bin/HelpmeClean.app ~/HelpmeClean.app
```


Finally, the last thing we need to do is to make sure Pi automatically log into Desktop without password.

```bash

sudo raspi-config

# System Options > Boot Auto login > Console Autologin

sudo reboot # to test

```

Done!

## If you want to test the scripts [Planed and not available yet]

I also ship a test program that automatically tests all your scripts in the `TorrentialPi` folder.

```bash
/usr/bin/python3 ./bin/unitTest.py
```

> It will display the result of every script and file test.


## After Setup

#### Remote Acess

You can get remote access via SSH always but if you want Desktop too then you can have that via VNC. For this, you have to refer VNC guide online. Once set up to turn on or off VNC as you wish but make sure to turn off after use as it takes considerable resources.

#### Log files

Log file is saving every step so very soon it would get very big to clear or if you want log files emailed to you - you can do it from `ClearLog.app` in `~`

> While SSH opens you in `~` but you are not in `~` then `cd ~`

```bash
./ClearLog.app
```



If you want to view it, it is located at:

```bash
~/TorrentialPi/Status_and_Logs/Scripts/Scripts.log
```




#### Cleaning Recommendation

It is advised to keep checking on storage and if you ever wants to know which are best to remove (least usefull) run:

```bash
~/HelpmeClean.app
```

