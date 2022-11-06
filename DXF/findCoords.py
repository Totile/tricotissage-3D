from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time
import numpy as np
import pyfirmata
import time
PI = 3.14

#control definition
mc = MyCobot("/dev/ttyACM0", 115200) #chmod 666 /dev/ttyACM0 à run avant
print(mc.is_power_on())

#initialisation process for arm
mc.send_angles([0,0,0,0,0,0], 50)
time.sleep(3)
coords = mc.get_coords()
print(f"null position {mc.get_coords()}")

mc.send_coords([-300, 0, 300, -105, 0, -90], 40)
time.sleep(3)
print(f"coords for base position {mc.get_coords()}")

print("releasing servo in 2 sec, be ready")
mc.release_all_servos()

while True:
    print(mc.get_coords())
    time.sleep(1)