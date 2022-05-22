#!/bin/bash
mv config.txt config_old.txt
pip3 install telegram paho-mqtt #python-telegram-bot
#sudo apt-get install mosquitto
echo Provide the username of the current user
read username
echo Choose a name for the new folder of the video files
read folder_name
mkdir $folder_name
echo Paste the API Key for the Telegram bot, for more info:
echo https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq#step-1-set-up-your-bots-profile
read api_key
echo Paste the User ID of the user or group that the bot will send the notifications and videos to, for more info:
echo "https://www.alphr.com/telegram-find-user-id/#:~:text=When%20you've%20located%20%40userinfobot,and%20the%20language%20of%20choice."
read user_id
echo "[SERVER]
ServerUsername = $username
VideoDestination = $folder_name
APIKey = $api_key
TelegramUserID = $user_id" >> config.txt