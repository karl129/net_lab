# UDPPingerServer.py 
from socket import * 

########## Begin ##########

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

########## End ##########

print( serverSocket)
