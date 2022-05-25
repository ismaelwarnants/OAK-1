# OAK-1 Bachelorproef: End-to-end system for low-cost fall detection using an OAK-1 camera
With this end-to-end system, an OAK-1 and a Raspberry Pi can be used to detect a fall.

To set up, just run the setup_node.sh or setup_server.sh

# FAQ

## How to solve X-LINK_UNBOOTED error: 
https://docs.luxonis.com/en/latest/pages/troubleshooting/#udev-rules-on-linux

echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules

sudo udevadm control --reload-rules && sudo udevadm trigger

## How to solve no_background:

export MESA_GL_VERSION_OVERRIDE=4.5
