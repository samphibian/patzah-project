The Patzah Project is a robotic platform designed to teach programming.
 * Controller components:
   * Raspberry Pi
   * GrovePi
   * Adafruit Servo HAT
 * Sensors/actuators:
   * Grove
   * Grove Cable + jumper cables + any other
   
*Please note that this repository includes the folders CADfiles and projectInformation which are not necessary to download.*

### For IP display and launch of jupyter server on startup:

#### Run:

sudo crontab -e

#### Add the following commands:

@reboot sleep 15 && sh /home/pi/displayAddress.sh >/home/pi/logs/cronlogIP 2>&1

@reboot sh /home/pi/launchJupyterServer.sh >/home/pi/logs/cronlogShell 2>&1
