import socket

print("服务开启")
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.43.66"
port = 8888 #自己定义的端口号

mySocket.bind((host, port))
mySocket.listen(10)
