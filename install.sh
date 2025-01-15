#!/bin/bash

# Make app.py executable
chmod +x app.py

# Create symbolic link
sudo ln -sf "$(pwd)/app.py" /usr/local/bin/cli-mate

echo "CLI-mate has been installed successfully!"
echo "You can now run it from anywhere using the 'cli-mate' command."