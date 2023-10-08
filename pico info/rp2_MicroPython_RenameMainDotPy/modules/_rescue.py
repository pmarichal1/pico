import machine
import os
import time

Pin = machine.Pin
led = Pin(25, Pin.OUT)
led.low()

def FileExists(filename):
  try:
    f = open(filename, "r")
    f.close()
    return True
  except:
    return False

if FileExists("main.py"):
  n = 1
  while FileExists("main-" + str(n) + ".py"):
    n = n + 1
  os.rename("main.py", "main-" + str(n) + ".py")
  s = "Renamed 'main.py' as 'main-" + str(n) + ".py'"
else:
  s = "No 'main.py' found"
  if FileExists("main-1.py"):
    n = 1
    while FileExists("main-" + str(n+1) + ".py"):
      n = n + 1
    s = "Renamed 'main.py' as 'main-" + str(n) + ".py'"

n = 0
try:
  while True:
    if n == 0:
      print("")
      print("This is the RenameMainDotPy firmware")
      print("")
    print(s)
    for nn in range(10):
      led.toggle()
      time.sleep(0.25)
    time.sleep(1)
    n = ( n + 1) % 5
except KeyboardInterrupt:
  pass

led.low()
print("")
print("====================================")
