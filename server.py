import socket
import sys

if(len(sys.argv) != 2):
    print("need port number")
    exit(0)

hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
UDP_PORT = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

print("server is running")

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

    if(handle in users):
        print("duplicate user " + handle)
        return ("FAILURE @" + handle + " is not registered").encode("utf-8")

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

    output = "SUCCESS @" + handle + " is registered"
    return output.encode("utf-8")
def query():
    # query handles
    # get number and list of all users
    output = "SUCCESS " + str(len(users)) + " "
    for key in users:
        output += key + " "

    return output.encode('utf-8')


def follow(input):
    # follow @<handle1> @<handle2>
    # add handle 1 to list of handle 2's followers and keep that list sorted
    # add handle 2 to lest of handle 1's follows
    handle1 = inputs[1][1:]
    handle2 = inputs[2][1:]

    if(handle1 == handle2):
        print("cannot follow itself")
        return ("FAILURE @" + handle1 + " could not follow itself").encode("utf-8")

    if(not handle2 in users):
        print("user @" + handle2 + " does not exist")
        return ("FAILURE @" + handle1 + " could not follow @" + handle2).encode("utf-8")

    for handle in followers[handle2]:
        if(handle == handle1):
            print(f"@{handle1} already follow @{handle2}")
            return (f"FAILURE already follows @{handle2}").encode("utf-8")

    followers[handle2].append(handle1)
    followers[handle2].sort()

    follows[handle1].append(handle2)

    output = "SUCCESS @" + handle1 + " followed @" + handle2
    return output.encode("utf-8")

def drop(input):
    # drop @<handle1> @<handle2>
    # remove handle 1 from handle 2's followers
    # remove handle 2 from handle 1's follows
    handle1 = inputs[1][1:]
    handle2 = inputs[2][1:]

    if(not handle2 in users):
        print(f"@{handle2} does not exist")
        return (f"FAILURE @{handle2} does not exist").encode("utf-8")

    found = False
    for handle in followers[handle2]:
        if (handle == handle1):
            found = True
            break

    if(not found):
        print(f"@{handle1} does not follow @{handle2}")
        return (f"FAILURE @{handle2} is not followed").encode("utf-8")

    followers[handle2].remove(handle1)
    follows[handle1].remove(handle2)

    output = "SUCCESS @" + handle1 + " unfollowed @" + handle2
    return output.encode("utf-8")

def exitUser(input):
    # exit @<handle>
    # remove user from any followers lists
    # remove user from users list, and remove user from follows and folllowers
    handle = inputs[1][1:]
    for f in follows[handle]:
        followers[f].remove(handle)

    for f in followers[handle]:
        follows[f].remove(handle)

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

    # match message with correct input and build the reply message
    if inputs[0] == "register" and len(inputs) == 6:
        reply = register(inputs)

    elif inputs[0] == "query" and inputs[1] == "handles":
        reply = query()

    elif inputs[0] == "follow" and len(inputs) == 3:
        reply = follow(input)

    elif inputs[0] == "drop" and len(inputs) == 3:
        reply = drop(input)

    elif inputs[0] == "exit" and len(inputs) == 2:
        reply = exitUser(input)

    elif inputs[0] == "print":
        reply += query() + followss()

    else:
        reply = b"bad request"

    # send reply back
    sock.sendto(reply, (addr))
