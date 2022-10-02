import socket

UDP_IP = socket.gethostname()
print(UDP_IP)
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

users = dict()
followers = dict()
follows = dict()

def register(inputs):
    # register @<handle> <IPv4-address> <port1> <port2> <port3>
    handle = inputs[1][1:]
    IP = inputs[2]
    port1 = inputs[3]
    port2 = inputs[4]
    port3 = inputs[5]

    print("user" + handle + "registers" + IP + port1 + port2 + port3)

    users[handle] = list()
    followers[handle] = list()
    follows[handle] = list()

    users[handle].append(IP)
    users[handle].append(port1)
    users[handle].append(port2)
    users[handle].append(port3)

    for key in users:
        print(key, users[key])

    output = "@" + handle + " is registered"
    return output.encode("utf-8")
def query():
    # query handles
    # get number and list of all users
    output = str(len(users)) + " "
    for key in users:
        output += key + " "

    return output.encode('utf-8')


def follow(input):
    # follow @<handle1> @<handle2>
    # add handle 1 to list of handle 2's followers and keep that list sorted
    handle1 = inputs[1][1:]
    handle2 = inputs[2][1:]

    followers[handle2].append(handle1)
    followers[handle2].sort()

    follows[handle1].append(handle2)

    output = "@" + handle1 + " followed @" + handle2
    return output.encode("utf-8")

def drop(input):
    # drop @<handle1> @<handle2>
    handle1 = inputs[1][1:]
    handle2 = inputs[2][1:]

    followers[handle2].remove(handle1)
    follows[handle1].remove(handle2)

    output = "@" + handle1 + " unfollowed @" + handle2
    return output.encode("utf-8")

def exitUser(input):
    # exit @<handle>
    handle = inputs[1][1:]
    for f in follows[handle]:
        followers[f].remove(handle)

    del followers[handle]
    del follows[handle]
    del users[handle]

    output = "@" + handle + " was removed"
    return output.encode("utf-8")


def followss():
    output = ""
    for key in followers:
        output += key + " " + str(followers[key])
    return output.encode("utf-8")

while True:
    msg, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    msg = msg.decode("utf-8")
    print("received message: " + msg)
    inputs = msg.split()
    print(inputs[0])
    reply = b""

    if inputs[0] == "register":
        reply = register(inputs)

    elif inputs[0] == "query":
        reply = query()

    elif inputs[0] == "follow":
        reply = follow(input)

    elif inputs[0] == "drop":
        reply = drop(input)

    elif inputs[0] == "exit":
        reply = exitUser(input)

    elif inputs[0] == "print":
        reply += query() + followss()
    else:
        reply = b"bad request"

    # send reply
    sock.sendto(reply, (addr))
