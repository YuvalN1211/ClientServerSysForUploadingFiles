import socket

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
conn, address = server_socket.accept()
print("Connection from: " + str(address))
