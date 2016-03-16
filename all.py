import time
import pyupm_grove as grove
import pyupm_i2clcd as lcd
from socketIO_client import SocketIO, BaseNamespace

class SensorNamespace(BaseNamespace):
    def on_connect(self):
        print('[Connected]')

socketIO = SocketIO('antoniohernandez.me', 8000)
sensor_socket = socketIO.define(SensorNamespace, '/sensor')

# Create the buttons
buttonInp = grove.GroveButton(3)
buttonInp2 = grove.GroveButton(7)
buttonOut = grove.GroveButton(4)
buttonOut2 = grove.GroveButton(8)
available = capacity = 21
bandera=True
# Initialize Jhd1313m1 at 0x3E (Lcd address)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
# RGB Blue
myLcd.setColor(255, 55, 0)


# Read the input and print, waiting one second between readings
while 1:
    if buttonInp.value() == 1 or buttonInp2==1:
        available= available - 1
        if available<0:        
            sensor_socket.emit('signal', {'area' : 'A', 'availability' :
0,'capacity' : capacity })
        else:
            sensor_socket.emit('signal', {'area' : 'A', 'availability' :
available,'capacity' : capacity })
        bandera=True
    if buttonOut.value() == 1 or buttonOut2==1:
        available=available + 1
        if available<0:
            sensor_socket.emit('signal', {'area' : 'A', 'availability' :
0,'capacity' : capacity })
        else:
            sensor_socket.emit('signal', {'area' : 'A', 'availability' :
available,'capacity' : capacity })
        bandera=True
    if bandera:
        myLcd.setCursor(0,0)
        myLcd.write('Disponibles:')
        myLcd.setCursor(1,0)
        myLcd.write('ZonaA')
        myLcd.setCursor(1,6)
        if available<0:
            myLcd.write('0')
        else:
            if available<10:
                myLcd.setCursor(1,6)
                myLcd.write('0')
                myLcd.setCursor(1,7)
            myLcd.write(str(available))
       myLcd.setCursor(1,9)
        myLcd.write('Lugares')
        bandera=False
    time.sleep(.5)
# Delete the button object del button
#delete buttonInp
#delete buttonInp2
#delete buttonOut
#delete buttonOut2

