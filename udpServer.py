import socket
import time
import random

#------------------------------------------
# transmit if id player that was hit

broadcaster = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def broadcast(target_id):
    broadcaster.sendto(str(target_id).encode(), ("127.0.0.1", 7500))

#------------------------------------------
# listen to hits

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 7501))

while True:
    data = sock.recvfrom(6)
    data_str = data[0].decode("latin-1")
    hit_data = data_str.split(":")
    shooter_id = int(hit_data[0]) # person who shoots
    target_id = int(hit_data[1]) # person who gets hit

    broadcast(target_id)
