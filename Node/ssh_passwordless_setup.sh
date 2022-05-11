#!/bin/bash

ssh-keygen -t rsa -b 4096
echo Provide the username to authenticate to the server
read username
echo Provide the ip address of the server
read server_ip_address
ssh-copy-id $username@$server_ip_address