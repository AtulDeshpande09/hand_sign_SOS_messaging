import socket

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(type(ip_address))
    return ip_address

print("your ip is : ",get_ip_address())