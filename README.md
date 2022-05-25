# End-to-end system for low-cost fall detection using an OAK-1 camera
With this end-to-end system, an OAK-1 and a Raspberry Pi (=Node) can be used to detect a fall.

Before proceeding, it is advised to make all files executable in this repo.
```
sudo chmod +x -R OAK-1
```

# Setup

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
To be added...

# FAQ

## How to solve: X-LINK_UNBOOTED error
https://docs.luxonis.com/en/latest/pages/troubleshooting/#udev-rules-on-linux
```
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules

sudo udevadm control --reload-rules && sudo udevadm trigger
```
## How to solve: AttributeError: 'NoneType' object has no attribute 'background_color' GLXBadFBConfig
Run this command each time before running the main.py code on the Node. It is also possible to place this variable in the .bashrc file in the home folder.

This error only seemed to happen on the Raspberry Pi 4B during testing, but it could happen on other single board computers.
```
export MESA_GL_VERSION_OVERRIDE=4.5
```
