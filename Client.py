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

def send_file_size(path):
    file_size = os.stat(path).st_size
    encoded_file_size = str(file_size).encode()
    print(f"{file_size} - {encoded_file_size}")
    client_socket.send(encoded_file_size)

def send_file_to_server(path):
    send_file_size(path)

    f = open(path, "rb")
    data = f.read(1024)
    while data:
        client_socket.send(data)
        data = f.read(1024)

def download_file_from_server(file_name):
    pass



def send_file_name(string):
    file_name = str(input(f"Enter the file name {string} (including type, like: my_file.txt)"))
    client_socket.send(file_name.encode())
    return file_name

def user_function():
    q = str(input("Do you want to upload or download a file? (u/d)"))
    if q == "u":
        client_socket.send(q.encode())
        send_file_name("to upload")

        file_path = str(input("Enter file path to a file you want to upload: "))
        send_file_to_server(file_path)

    elif q == "d":
        client_socket.send(q.encode())
        file_name = send_file_name("to download")
        
        download_file_from_server(file_name)
    else:
        print("Expected (u/d)")


user_function()