#!/bin/bash

if [ "$UID" -ne 0 ] 
	then 
	echo "Please run as root"
	exit
fi

# Copy the config file to ~/.config
mkdir -p ~/.config/ggl/
cp ggl.config ~/.config/ggl/ggl.config

# Copy the script to /usr/bin
cp ggl.py /usr/bin/ggl
