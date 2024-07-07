#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM) 
#Prepare a sever socket 
########## Begin ##########
# bind 接受一个元组
serverSocket.bind(('127.0.0.1', 6789))
serverSocket.listen(1)
########## End ##########
print(serverSocket)
serverSocket.close()