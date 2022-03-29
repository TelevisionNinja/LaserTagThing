import socket

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 7501))

while True:
    data = sock.recvfrom(6)
    data_str = data[0].decode("latin-1")
    shooter_id = int(data_str.split(":")[0]) # person who shoots
    target_id = int(data_str.split(":")[1]) # person who gets hit
    print(f"id of player who shot: {shooter_id}")
    print(f"id of player who was hit: {target_id}")