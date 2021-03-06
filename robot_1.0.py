from inputs import devices
from robot import Robot
from AX12 import AX12
from inputs import get_gamepad
import time

pos_init = 30
pos_attq = 120
pos_arriere = 0

bridage_g = 0.5
bridage_d = 0.5

r = Robot()
r.add_object(AX12(174), "roue_gauche")
r.add_object(AX12(173), "roue_droite")
r.add_object(AX12(162), "fleau")

##### SEQUENCE
r.add_sequence("seq_1")

r.roue_gauche.turn(0)
r.roue_droite.turn(0)

    
def deplacement():

	direction = 0
	speed = 0
	direction = 0
	
	while 1:
		
		time.sleep(0.01)

		events = [event for event in get_gamepad() if event.ev_type == 'Absolute' or event.ev_type == "Key"]
		for event in events:

			if event.ev_type == 'Absolute' and event.code in ['ABS_RZ','ABS_Z','ABS_X']:
				
				if event.code == 'ABS_RZ': #Accelerateur
					
					trigger = event.state
					speed  = (trigger * 100) / 255

				if event.code == 'ABS_Z': #Marche arriere

                                	trigger = event.state
                                	speed  = - (trigger * 100) / 255

				if event.code == 'ABS_X': #Direction
				
					direction = event.state
				
				if speed == 0:

					speed_g = - direction // 65280
					speed_d = - direction // 65280
	
				elif direction <= 0:
						
					speed_g = (speed * (32640 + direction)) // 16320
					speed_d = - speed

				else:
					
					speed_d = - (speed * (32640 - direction)) // 16320
					speed_g = speed

				try:
						
					r.roue_gauche.turn(speed_g)	
					r.roue_droite.turn(speed_d)

				except:
					pass

			if (event.ev_type, event.code) == ('Key', 'BTN_SOUTH'): #fleau digital
				
				if event.state == 0:
				
					try:
						r.fleau.move(pos_init)
					except:
						pass

				if event.state == 1:
					
					try:
						r.fleau.move(pos_attq)
					
					except:					
						pass

			if (event.ev_type, event.code) == ('Absolute', 'ABS_RY'):
				
				valeur = event.state #entre -32640 et 32640
				
				if valeur <= 0:
					
					position = pos_init - ((pos_attq - pos_init) * valeur) // 32640
				
				else:
					
					position = pos_init - ((pos_init - pos_arriere) * valeur) // 32640
			
				try:
					r.fleau.move(position)
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
