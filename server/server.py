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
clients_num = 0

last_move_white = ""
last_move_black = ""
end = False

def threaded_client(connection):
    global currentId, last_move_white, last_move_black, end, clients_num
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
                if reply == "WAITING":
                    if clients_num < 2:
                        reply = "WAITING"
                    if clients_num == 2:
                        reply = "START"
                elif reply == "END":
                    end = True
                else:
                    params = reply.split(":")
                    if params[0] == "W":
                        last_move_white = params[1]
                    elif params[0] == "B":
                        last_move_black = params[1]
                    reply = last_move_white + ":" + last_move_black
                if end:
                    reply = "END"
                connection.sendall(str.encode(reply))

        except error as e:
            print(str(e))
            break

    print("Connection Closed")
    clients_num -= 1
    connection.close()


while True:
    connection, address = s.accept()
    print("Connected to: ", address)
    end = False
    clients_num += 1
    start_new_thread(threaded_client, (connection, ))
