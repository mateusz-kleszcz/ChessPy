import socket
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 8080

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error:
    print(str(socket.error))

s.listen(2)
print("Waiting for a connection", server_ip)

currentId = "0"
pos = ["0:50,50", "1:100,100"]


def threaded_client(connection):
    global currentId, pos
    connection.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = connection.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                connection.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                nid = -1
                if id == 0:
                    nid = 1
                if id == 1:
                    nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)

            connection.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    connection.close()


while True:
    connection, address = s.accept()
    print("Connected to: ", address)

    start_new_thread(threaded_client, (connection, ))
