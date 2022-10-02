import socket

UDP_IP = "Timmys-MacBook-Pro.local"
UDP_PORT = 5005
msg = b"register @a 127.23.12.34 23423 93423 21321"
#msg = b"register @b 001.22.33.44 334 432 654"
#msg = b"register @c 999.99.99.99 dsf ffd fds"
#msg = b"query handles"
#msg = b"follow @c @b"
#msg = b"follow @a @b"
#msg = b"print"
#msg = b"drop @a @b"
#msg = b"exit @b"
#msg = b"print"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(msg, (UDP_IP, UDP_PORT))
reply, addr = sock.recvfrom(1024)
reply = reply.decode("utf-8")
print("received message: " + reply)