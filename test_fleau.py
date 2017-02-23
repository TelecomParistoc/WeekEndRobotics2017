from robot import Robot
from AX12 import AX12
import time


#pos_init=46
#pos_choc=114
r = Robot()
r.add_object(AX12(142), "fleau")

#r.fleau.move(pos_choc)
#time.sleep(1.0)
#r.fleau.move(pos_init)

print(r.fleau.get_position())

r.stop()
