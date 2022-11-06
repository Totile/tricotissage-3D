#vbzevikzjbvkzej
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time
import numpy as np
import pyfirmata
import time
PI = 3.14

#utilitaries
def send_step(N, pin, milli, board):
    """In: send N step through the Pin"""
    for i in range(N):
        board.digital[pin].write(1)
        time.sleep(milli/1000000) #microseconds

        board.digital[pin].write(0)
        time.sleep(milli/1000000) #microseconds
    return None

def FLOAT(x):
    try:
        return float(x)
    except:
        return x
FLOAT = np.vectorize(FLOAT)

#control definition
board = pyfirmata.Arduino('/dev/ttyACM1')
mc = MyCobot("/dev/ttyACM0", 115200) #chmod 666 /dev/ttyACM0 à run avant
print(mc.is_power_on())

#initialisation process for arm
mc.send_angles([0,0,0,0,0,0], 50)
time.sleep(3)
print(f"null position {mc.get_coords()}")

mc.send_coords([288, -30, 300, -100, 0, -90], 40)
time.sleep(3)
print(f"coords for base position {mc.get_coords()}")

#test for steps to servo
send_step(100, 3, 400, board)
time.sleep(1)
print(f"sent 1000 steps")

#read instructions
with open("./command_orders.txt") as file:
    commands = file.readlines()
    for command in commands:
        command = command.strip()
        command = command.split(", ")
        command += [-100, 0, -90] #change head orientation
        command = FLOAT(command)
        command = command.tolist()
        print(command, command[0])
        if command[0] == "new_arete" or command[0] == "'new_arrete' '-100, '0' '-90'": #needs to repeat head orientation
            print(command)
            continue
        #mc.send_coords([188.04548429679977, -30.0, 283.7238571428571, -90.0, 0.0, -180.0], 20, 1)
        mc.send_coords(command, 40, 1)
        time.sleep(1)
        procede = input("do you wish to continue Y/n ? ")
        if procede == "n":
            break
        time.sleep(1)