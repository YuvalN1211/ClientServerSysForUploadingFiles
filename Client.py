import socket
import os

def get_socket_info():
    your_device = str(input("Are you trying to comunicate with a server that is on your device (y/n)"))
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

client_socket = socket.socket()
info = get_socket_info()
client_socket.connect(info)


    

def send_file(socket, path):

    file_size = os.stat(path).st_size
    encoded_file_size = str(file_size).encode("utf-8")
    print(f"{file_size} - {encoded_file_size}")
    socket.send(encoded_file_size)

    f = open(path, "rb")
    data = f.read(1024)
    while data:
        socket.send(data)
        data = f.read(1024)

file_path = str(input("Enter file path to a file you want to upload: "))
send_file(client_socket, file_path)