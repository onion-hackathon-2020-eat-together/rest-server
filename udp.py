import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("192.168.137.51", 5000))

data = sock.recvfrom(55555)