import socket
import math

def get_socket_info():
    your_device = str(input("Are you trying to comunicate with a client that is on your device (y/n)"))
    if your_device == "y":
        ip = "127.0.0.1"
    elif your_device == "n":
        ip = str(input("Enter the ip of the target you want to bind to: "))
    else:
        print("error: invalid answere, expected (y/n)")
        return get_socket_info()
    port = int(input("Enter port: "))
    info = (ip, port)
    return info

server_socket = socket.socket()
info = get_socket_info()
print(info)
server_socket.bind(info)
server_socket.listen(1)
print("Waiting for connections")
connected_socket, address = server_socket.accept()
print("Connection from: " + str(address))

def recive_data(socket, server_socket, path):
    file = open(path, "wb")
    file_size = int(connected_socket.recv(4).decode("utf-8"))
    
    
    print(f"file size is {file_size} bytes")
    i = math.ceil(file_size / 1024)
        
    while i > 0:
        chunk = socket.recv(1024)
        print(f"\nWriting {chunk}\n")
        file.write(chunk)
        i -= 1



    # while(True):
    #     chunk = socket.recv(1024)
    #     if not chunk:
    #         print("no content")
    #         break
    #     else:
    #         print(f"Writing {chunk}")
    #         file.write(chunk)


recive_data(connected_socket, server_socket, r"C:\Users\yuval\OneDrive\אקדמיית_המתכנתים\רשתות_תקשורת_ופרוטוקולים\ClientServerSysForUploadingFiles\ServerStorage.txt")