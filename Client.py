import socket
import os
import math
import sys


print("Client\n-----------")

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

# make socket
client_socket = socket.socket()
info = get_socket_info()
client_socket.connect(info)

# upload function 2
def send_file_size(path):
    file_size = os.stat(path).st_size
    byte_data = file_size.to_bytes(4, byteorder='big')
    client_socket.send(byte_data)

# upload function 1
def send_file_to_server(path):
    send_file_size(path)

    f = open(path, "rb")
    data = f.read(1024)
    while data:
        client_socket.send(data)
        data = f.read(1024)


# download function
def download_file_from_server(path):
    file = open(path, "wb")
    recive_bytes = client_socket.recv(4)
    file_size = int.from_bytes(recive_bytes, byteorder='big')
    
    print(f"file size is {file_size} bytes")
    i = math.ceil(file_size / 1024)
        
    while i > 0:
        chunk = client_socket.recv(1024)
        file.write(chunk)
        i -= 1
    print("finished writing")


# function for sending the name for the server, upload and download
def send_file_name(string):
    file_name = str(input(f"Enter the file name {string} (including type, like: my_file.txt): "))
    length = str(len(file_name))
    print(f"length of name: {length}")
    client_socket.send(length.encode())
    client_socket.send(file_name.encode())
    return file_name

def main():
    q = str(input("Do you want to exit, upload or download a file? (e/u/d): "))
    if q == "u":
        client_socket.send(q.encode())
        send_file_name("to upload")

        file_path = str(input("Enter file path to a file you want to upload: "))
        send_file_to_server(file_path)
        main()

    elif q == "d":
        client_socket.send(q.encode())
        file_name = send_file_name("to download")
        
        file_path = str(input("Enter path to a directory you want to download to: "))
        path = f"{file_path}\{file_name}"
        download_file_from_server(path)
        main()
    elif q == "e":
        client_socket.send(q.encode())
        sys.exit()

    else:
        print("Expected (e/u/d)")
        main()


main()