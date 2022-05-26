# End-to-end system for low-cost fall detection using an OAK-1 camera
With this end-to-end system, an OAK-1 and a Raspberry Pi can be used to detect a fall.
![image](https://user-images.githubusercontent.com/22435080/170510964-5c70b207-acd8-400e-b82e-8bd3dd0a2d12.png)
In this image, the node is a Raspberry Pi 4 with an OAK-1 camera, and the client is the healthcare personnel.

NOTE: This is a proof of concept, this means that the system is not ready for production use and that the fall detection is only built for demonstration purposes only.

# Setup
Before proceeding, it is advised to make all files executable in this repo.
```
sudo chmod +x -R OAK-1
```

To set up there is a script for the Node and for the Server.


## Server Setup
The server has to have ssh, python 3.8 or 3.9 and pip installed and running.

Afterwards, the setup_server.sh script can be ran to prepare the system.
```
./setup_server.sh
```
or

```
bash setup_server.sh
```

NOTE: Some operating systems require to use python and pip instead of python3 and pip3 respectively, this has to be changed in the install_requirements.sh file before running the setup script.

Once finished, the code can be started by using following command:
```
python3 main.py
```

### Only installing the requirements, without the setup
This script will install all the required dependencies and setup the required configuration.
If you only want to install the requirements, then use the install_requirements.sh file.
```
./install_requirements.sh
```
or

```
bash install_requirements.sh
```

## Node setup
The node has to have python 3.8 or 3.9 and pip installed and running.

Afterwards, the setup_node.sh script can be ran to prepare the system.
```
./setup_node.sh
```
or

```
bash setup_node.sh
```
NOTE: Some operating systems require to use python and pip instead of python3 and pip3 respectively, this has to be changed in the install_requirements.sh file before running the setup script.

### Notes during installation:
To setup the Node, the first questions can be ignored by pressing enter, these questions are to set up passwordless authentication to the server.

It is required to fill in the details to authenticate to the server, the password will only be asked to authenticate once.

The user that will be used to authenticate to the server requires basic read/write permissions of the folder where the videos will be stored.

The folder name is chosen during the setup script of the server and will be put in the home folder of the user.

Once finished, the code can be started by using following command:
```
python3 main.py
```

### Only installing the requirements, without the setup
This script will install all the required dependencies and setup the required configuration.
If you only want to install the requirements, then use the install_requirements.sh file.
```
./install_requirements.sh
```
or

```
bash install_requirements.sh
```

# Parts of the system that can be improved

## Recording quality can be set at 720p
For now the recording quality was set at 480p, because a 20 second clip at 720p exceeded the 50 MB file that a Telegram bot can send at once.
This upload limit (per file), can be extended to 2 GB/file when you set up your own server for the bot.
https://core.telegram.org/bots/api#using-a-local-bot-api-server

## Recording instablity with some micro sd cards
Some micro sd cards can cause stability issues with the recording speed. This is probably due to some micro sd cards not being fast enough to write the frame, even at 480p. This slows down the frames per second that can be written. Because of this, the video that normally expects 20 fps, will now create a video shorter video with the frames that are rendered.

To solve this, an ssd or similar storage could be used. 

Or the files could be written in the /tmp folder, which is located in ram. But this solution requires more complex video storage management and will cause data loss when the power is lost.

## Reliability
At this moment, the system does not check for failures in sending the data. This should be done at every stage (mqtt, sftp, ...).

There is also nothing implemented for a fallback server in case a server requires maintance or has an issue.

## Dependance on an active internet connection
By using Telegram, we depend on an active internet connection to notify the healtcare personnel. This has the advantage that they can receive the message on any network in any place. However, if the internet connection of the server is disconnected, healthcare personnel do not receive notifications.

To prevent this, a fallback system could be created to immediately take over on the local network, this system could also replace the Telegram bot.

# FAQ

## How to solve: X-LINK_UNBOOTED error
https://docs.luxonis.com/en/latest/pages/troubleshooting/#udev-rules-on-linux
```
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules

sudo udevadm control --reload-rules && sudo udevadm trigger
```
## How to solve: AttributeError: 'NoneType' object has no attribute 'background_color' GLXBadFBConfig
Run this command each time before running the main.py code on the Node. It is also possible to place this variable in the .bashrc file in the home folder.

This error only seemed to happen on the Raspberry Pi 4B with Raspberry Pi OS during testing, but it could happen on other single board computers.
```
export MESA_GL_VERSION_OVERRIDE=4.5
```
