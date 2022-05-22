#!/bin/bash
# Source: https://linuxize.com/post/how-to-setup-passwordless-ssh-login/
mv config.txt config_old.txt
ssh-keygen -t rsa -b 4096
echo Provide the username to authenticate to the server
read username
echo Provide the ip address of the server
read server_ip_address
ssh-copy-id $username@$server_ip_address
echo Select the destination folder for the videos on the server
read folder_name
echo Please provide the room number
read room_nr
if [ -z "$room_nr" ]
then
      room_nr="0"
fi
echo "[NODE]
ServerIP = $server_ip_address
ServerUsername = $username
VideoDestination = $folder_name
RoomNR = $room_nr" >> config.txt