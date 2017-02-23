from inputs import devices
from robot import Robot
from AX12 import AX12
from inputs import get_gamepad
import time

pos_init = -48
pos_attq = 10

pos_init_ballon= 50
pos_arriere_ballon = 100

bridage_g = 1
bridage_d = 1

r = Robot()
r.add_object(AX12(174), "roue_gauche")
r.add_object(AX12(173), "roue_droite")
r.add_object(AX12(162), "ballon")
r.add_object(AX12(142),"fleau")

##### SEQUENCE
r.add_sequence("seq_1")

r.roue_gauche.turn(0)
r.roue_droite.turn(0)
r.ballon.move(pos_init_ballon)

    
def deplacement():

	direction = 0
	speed = 0
	pos_ballon = pos_init_ballon

	while 1:
		
		time.sleep(0.01)

		events = [event for event in get_gamepad() if event.ev_type == 'Absolute' or event.ev_type == "Key"]
		for event in events:
				
			if event.code == 'ABS_RZ': #Accelerateur
					
				trigger = event.state
				speed  = (trigger * 100) / 255

			if event.code == 'ABS_Z': #Marche arriere

                                trigger = event.state
                                speed  = - (trigger * 100) / 255

			if event.code == 'ABS_X' : #Direction
				
				direction = event.state
				#print(direction)
	
			if event.code == 'BTN_TL' and event.state == 1: #tourner sur soi

                                speed_g = - 100
                                speed_d = - 100

			elif event.code == 'BTN_TR' and event.state == 1:

				speed_g = 100
				speed_d = 100
			
			elif direction <= 0:

				#print("rotation gauche")
				speed_g = (speed * (32640 + direction)) // 16320
				speed_d = - speed

			else:

				#print("rotation droite")
				speed_d = - (speed * (32640 - direction)) // 16320
				speed_g = speed

			try:
						
				r.roue_gauche.turn(int(speed_g*bridage_g))	
				r.roue_droite.turn(int(speed_d*bridage_d))

			except:
				pass

			if event.code == 'BTN_SOUTH': #fleau
				
				if event.state == 0:
				
					position = pos_init

				else:
					
					position = pos_attq

				try:

					r.fleau.move(position)

				except:
					pass

			if event.code == 'BTN_NORTH': #Reculer le ballon
				
				if event.state == 1:
					
					if pos_ballon == pos_init_ballon:

						pos_ballon = pos_arriere_ballon

					else:

						pos_ballon = pos_init_ballon
			
				try:

					r.ballon.move(pos_ballon)

				except:
					pass
					
		

def speed_direction(speed, direction):
	
	if direction == 0:

		return(speed, - speed)
	
	if direction == -1:

		return(speed // 2, - speed)
	
	if direction == 1:
	
		return(speed, - speed//2)


r.add_parallel(deplacement, [], False)
r.wait() 
r.sequence_done()

#####


r.start_sequence('seq_1')
r.wait_sequence()
r.stop()
