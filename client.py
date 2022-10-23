import socket
import sys

# allow user to pass in server IP
if(len(sys.argv) != 3):
    print("need both server IP and port number")
    exit(0)

tweets = dict() # who following to left and right neighbors

UDP_IP = sys.argv[1] #input("please enter server IP\n") # Timmys-MacBook-Pro.local
UDP_PORT = int(sys.argv[2])
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# have user make a handle name and go ahead and register it
handle = input("enter a handle (without the @)\n")

port1 = int(input("enter port number 1"))
port2 = int(input("enter port number 2"))
port3 = int(input("enter port number 3"))
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

print(IP)

serverSock.sendto(f"register @{handle} {IP} {port1} {port2} {port3}".encode("utf-8"), (UDP_IP, UDP_PORT))

reply, addr = serverSock.recvfrom(1024)
reply = reply.decode("utf-8")

print("received message: " + reply)

replyArray = reply.split()
if(replyArray[0] == "FAILURE"):
    print("please restart with a unique handle")
    exit(0)

msg = ""
userIn = ""

""""
msg = b"register @a 127.23.12.34 23423 93423 21321"
msg = b"register @b 001.22.33.44 334 432 654"
msg = b"register @c 999.99.99.99 dsf ffd fds"
msg = b"query handles"
msg = b"follow @c @b"
msg = b"follow @a @b"
msg = b"print"
msg = b"drop @a @b"
msg = b"print"
msg = b"exit @b"
msg = b"print"
"""

# allow user to pass in command
while(userIn != "exit") :
    userIn = input("please enter a command\n")
    inputs = userIn.split()

    if(inputs[0] == "follow" and len(inputs) == 2):
        msg = f"follow @{handle} {inputs[1]}".encode("utf-8")

    elif(inputs[0] == "drop" and len(inputs) == 2):
        print(inputs[1])
        msg = f"drop @{handle} {inputs[1]}".encode("utf-8")

    elif (inputs[0] == "exit" and len(inputs) == 1):
        msg = f"exit @{handle}".encode("utf-8")

    elif (inputs[0] == "query"):
        msg = f"query handles".encode("utf-8")

    elif (inputs[0] == "query"):
        msg = f"tweet @{handle} {inputs[1]}".encode("utf-8")

    else:
        print("unknown command or poorly formatted command")
        continue

    serverSock.sendto(msg, (UDP_IP, UDP_PORT))

    reply, addr = serverSock.recvfrom(1024)
    reply = reply.decode("utf-8")

    print("received message: " + reply)