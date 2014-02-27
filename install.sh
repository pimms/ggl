#!/bin/bash

if [ "$UID" -eq 0 ] 
	then 
	echo "Do NOT run this script as root."
	exit
fi

# Copy the config file to ~/.config
# It's important that this command is not run as root
# so the config file is placed in the correct directory.
mkdir -p ~/.config/ggl/
if [ ! -f ~/.config/ggl/ggl.config ]; then
	echo "Copying config file..."
	cp ggl.config ~/.config/ggl/ggl.config
else
	echo "Config file exists, not overriding."	
fi


# Copy the script to /usr/bin as root.
echo "Copying executable script: root required"
sudo cp ggl.py /usr/bin/ggl
