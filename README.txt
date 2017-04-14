## For IP display and launch of jupyter server on startup:

### Run:

sudo crontab -e

### Add the following commands:

@reboot sleep 15 && sh /home/pi/displayAddress.sh >/home/pi/logs/cronlogIP 2>&1

@reboot sh /home/pi/launchJupyterServer.sh >/home/pi/logs/cronlogShell 2>&1