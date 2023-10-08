# A simple example that:
# - Connects to a WiFi Network defined by "ssid" and "password"
# - Performs a GET request (loads a webpage)
# - Queries the current time from a server
#import modules
import network
import socket
from time import sleep
from machine import Pin
import dht

sensor = dht.DHT11(Pin(28))

def read_dht():
  try:
    sleep(2)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    print('Temperature: %3.1f F' %temp_f)
    print('Humidity: %3.1f %%' %hum)
    return temp,hum
  except OSError as e:
    print('Failed to read sensor.')

ssid = 'SpectrumSetup-AC' #Your network name
password = 'winedrama832' #Your WiFi password

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(reading):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Pico W Weather Station</title>
            <meta http-equiv="refresh" content="10">
            </head>
            <body>
            <p>{reading}</p>
            </body>
            </html>
            """
    return str(html)
    
def serve(connection):
    #Start a web server
    
    while True:
        #temp, humidity = read_dht()
        #reading = 'Temperature: ' + temp + '. Humidity: ' + humidity
        #read_dht()
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)       
        html = webpage(reading)
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()