import socket
import os
import math
import sys

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
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = int(input("Enter port: "))
    info = (host_ip, port)
    return info

# make socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
info = get_socket_info()
print(f"info: {info}")
server_socket.bind(info)
server_socket.listen(1)
print("Waiting for connections")
connected_socket, address = server_socket.accept()
print("Connection from: " + str(address))

# upload function 2
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
    print(f"finished writing the file that was sent from {address}")

# upload function 1
def get_file_name_upload():
    bytes = int(connected_socket.recv(4).decode())
    file_name = connected_socket.recv(bytes).decode()
    return file_name


# download function 3
def send_file_size(path):
    file_size = os.stat(path).st_size
    byte_data = file_size.to_bytes(4, byteorder='big')
    connected_socket.send(byte_data)
    print(f"file size sent to {address}")

# download function 2
def send_data(path):
    send_file_size(path)

    f = open(path, "rb")
    
    data = f.read(1024)
    while data:
        connected_socket.send(data)
        data = f.read(1024)
    print(f"downloaded to {address}")

# download function 1
def get_file_name_download():
    in_storage_message = "file is in server storage"
    not_in_storage_message = "file is not in server storage, enter a valid file name"

    while True:
        bytes = int(connected_socket.recv(4).decode())
        file_name = connected_socket.recv(bytes).decode()
        if file_name in os.listdir(base_dir):
            print(in_storage_message)
            message_len = str(len(in_storage_message))
            connected_socket.send(message_len.encode())
            connected_socket.send(in_storage_message.encode())
            break
        else:
            print(not_in_storage_message)
            message_len = str(len(not_in_storage_message)).zfill(4)
            print(f"message length: {message_len}")
            connected_socket.send(message_len.encode())
            connected_socket.send(not_in_storage_message.encode())
        
    return file_name


def main():
    global base_dir
    while True:
        print("\n")
        q = connected_socket.recv(1).decode()
        
        if q == "u":
            file_name = get_file_name_upload()
            path = f"{base_dir}\{file_name}"

            print(f"path of file to upload {path}")
            recive_data(path)
        elif q == "d":
            file_name = get_file_name_download()
            path = f"{base_dir}\{file_name}"

            send_data(path)
        elif q == "e":
            connected_socket.close()
            server_socket.close()
            print("Goodbye")
            sys.exit()

main()