import socket
import os
import math

print("Server\n-----------")

# my computer or not for server storage directory
def Yuval_check():
    Yuval = str(input("Is this Yuval's computer? (y/n)"))
    if Yuval == "y":
        return r"C:\Users\yuval\OneDrive\אקדמיית_המתכנתים\רשתות_תקשורת_ופרוטוקולים\ClientServerSysForUploadingFiles\ServerStorage"
    elif Yuval == "n":
        base_dir = str(input("Enter path for a directory that will be the server storage: "))
        return fr"{base_dir}"
    else:
        print("error, expected (y/n)")
        Yuval_check()

base_dir = Yuval_check()

def get_socket_info():
    your_device = str(input("Are you trying to comunicate with a client that is on your device (y/n): "))
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
server_socket = socket.socket()
info = get_socket_info()
print(info)
server_socket.bind(info)
server_socket.listen(1)
print("Waiting for connections")
connected_socket, address = server_socket.accept()
print("Connection from: " + str(address))

# upload function
def recive_data(path):
    file = open(path, "wb")
    recive_bytes = connected_socket.recv(4)
    file_size = int.from_bytes(recive_bytes, byteorder='big')
    
    print(f"file size is {file_size} bytes")
    i = math.ceil(file_size / 1024)
        
    while i > 0:
        chunk = connected_socket.recv(1024)
        file.write(chunk)
        i -= 1
    print("finished writing")

# download function 2
def send_file_size(path):
    file_size = os.stat(path).st_size
    byte_data = file_size.to_bytes(4, byteorder='big')
    connected_socket.send(byte_data)

# download function 1
def send_data(path):
    send_file_size(path)

    f = open(path, "rb")
    
    data = f.read(1024)
    while data:
        connected_socket.send(data)
        data = f.read(1024)

# main help function
def get_file_name():
    bytes = int(connected_socket.recv(1).decode())
    file_name = connected_socket.recv(bytes).decode()
    return file_name


def main():
    global base_dir
    while True:
        q = connected_socket.recv(1).decode()
        file_name = get_file_name()
        path = f"{base_dir}\{file_name}"

        if q == "u":
            print(f"path of file to upload {path}")
            recive_data(path)
        elif q == "d":
            send_data(path)
        elif q == "e":
            connected_socket.close()
            server_socket.close()
            break

main()