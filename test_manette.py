from inputs import devices

for device in devices:
    
    print(device)
    
    
from inputs import get_gamepad
while 1:
     events = get_gamepad()
     for event in events:
         print(event.ev_type, event.code, event.state)
