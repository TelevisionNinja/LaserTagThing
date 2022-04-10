import socket

# socket setup
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 7501))


# emit id of player that was hit
def emitHit(target_id):
    sock.sendto(str(target_id).encode(), ("127.0.0.1", 7500))


# process the received data
def parseData(raw_data):
    data_str = raw_data[0].decode("latin-1")
    hit_data = data_str.split(":")
    shooter_id = int(hit_data[0]) # person who shoots
    target_id = int(hit_data[1]) # person who gets hit

    return shooter_id, target_id


# example callback function
def callback(shooter_id, target_id):
    print(str(shooter_id) + " shot " + str(target_id))


# listen to hits
while True:
    data = sock.recvfrom(6)
    shooter_id, target_id = parseData(data)

    emitHit(target_id)

    callback(shooter_id, target_id)
