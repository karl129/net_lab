#import socket module
from socket import *
import os

serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a sever socket 
serverSocket.bind(("127.0.0.1",6789))
serverSocket.listen(1)

#while True:
print('开始WEB服务...')

try:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024) # 获取客户发送的报文
        
    #读取文件内容
    ######### Begin #########
    file_name = str(message).split(' ', 2)[1][1:]
    with open(file_name, 'r') as f:
        outputdata = f.read()
    ######### End #########
    print(outputdata)
    connectionSocket.close()
except IOError:
        
    connectionSocket.close()
serverSocket.close()