#!/bin/bash
./ssh_passwordless_setup.sh
./install_requirements.sh
# To set up the OAK-1 camera: https://docs.luxonis.com/en/latest/pages/troubleshooting/#udev-rules-on-linux
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
echo Setup finished!
