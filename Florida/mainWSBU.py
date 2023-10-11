# class to handle WiFi conenction
import network
import socket
from NetworkCredentials import NetworkCredentials
from time import sleep
import machine
import dht
import rp2

rp2.country('US')
#setup on board LED
led = machine.Pin("LED", machine.Pin.OUT)
# setup PIN for DHT11
sensor = dht.DHT11(machine.Pin(28))

def read_dht(loopcnt):
  try:
    sleep(2)
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    tempF = temperature * (9/5) + 32.0
    print('Temperature: %3.1f F' %tempF)
    print('Humidity: %3.1f %%' %humidity)
    print(loopcnt)
    return tempF,humidity
  except OSError as e:
    print('Failed to read sensor.')
        
def new_web_page(temperature,humidity,loopcnt):
    html = """<html><head><meta http-equiv="refresh" content="5"><meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Helvetica", Arial;}
  table { border-collapse: collapse; width:55%; margin-left:auto; margin-right:auto; }
  th { padding: 12px; background-color: #87034F; color: white; }
  tr { border: 2px solid #000556; padding: 12px; }
  tr:hover { background-color: #bcbcbc; }
  td { border: none; padding: 14px; }
  .sensor { color:DarkBlue; font-weight: bold; background-color: #ffffff; padding: 1px;  
  </style></head><body><h1>Paul's Pi Pico W Weather Station</h1>
  <table><tr><th>Parameters</th><th>Value</th></tr>
  <tr><td>Temperature</td><td><span class="sensor">""" + str(temperature) + """</span></td></tr>
  <tr><td>Humidity</td><td><span class="sensor">""" + str(humidity) + """</span></td></tr>
  <tr><td>Requests</td><td><span class="sensor">""" + str(loopcnt) + """</span></td></tr> 
  
  </body></html>"""
    return html

def serve(connection):
    loopcnt=0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        led.value(1)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        #if request == '/getinfo?':
        loopcnt +=1
        temperature, humidity = read_dht(loopcnt)
        html = new_web_page(temperature,humidity,loopcnt)
        client.send(html)
        client.close()
        sleep(60)
        led.value(0)

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return(connection)
 
class WiFiConnection:
    # class level vars accessible to all code
    status = network.STAT_IDLE
    ip = ""
    subnet_mask = ""
    gateway = ""
    dns_server = ""
    wlan = None

    def __init__(self):
        pass

    @classmethod
    def start_station_mode(cls, print_progress=False):
        # set WiFi to station interface
        cls.wlan = network.WLAN(network.STA_IF)
        # activate the network interface
        cls.wlan.active(True)
        # connect to wifi network
        cls.wlan.connect(NetworkCredentials.ssid, NetworkCredentials.password)
        cls.status = network.STAT_CONNECTING
        if print_progress:
            print("Connecting to Wi-Fi - please wait")
        max_wait = 20
        # wait for connection - poll every 0.5 secs
        while max_wait > 0:
            """
                0   STAT_IDLE -- no connection and no activity,
                1   STAT_CONNECTING -- connecting in progress,
                -3  STAT_WRONG_PASSWORD -- failed due to incorrect password,
                -2  STAT_NO_AP_FOUND -- failed because no access point replied,
                -1  STAT_CONNECT_FAIL -- failed due to other problems,
                3   STAT_GOT_IP -- connection successful.
            """
            if cls.wlan.status() < 0 or cls.wlan.status() >= 3:
                # connection attempt finished
                break
            max_wait -= 1
            sleep(0.5)

        # check connection
        cls.status = cls.wlan.status()
        if cls.wlan.status() != 3:
            # No connection
            if print_progress:
                print("Connection Failed")
            return False
        else:
            # connection successful
            config = cls.wlan.ifconfig()
            cls.ip = config[0]
            cls.subnet_mask = config[1]
            cls.gateway = config[2]
            cls.dns_server = config[3]
            if print_progress:
                print('ip = ' + str(cls.ip))
            return True, cls.ip
try:
    status , ip = WiFiConnection.start_station_mode(True)
    print (status , ip)
    if not status:
    #if not WiFiConnection.start_station_mode(True):
         raise RuntimeError('network connection failed')        
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()