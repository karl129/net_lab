#ICMPPing.py

import socket
import os
import struct
import time
import select

ICMP_ECHO_REQUEST = 8

# 生成校验和
def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = str[count + 1] * 256 + str[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(str):
        csum = csum + str[len(str) - 1].decode()
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# 发送一次Ping数据包
def sendOnePing(mySocket, ID, sequence, destAddr):
    # 头部构成： type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    data = struct.pack("!d", time.time())
    # 计算头部和数据的校验和
    myChecksum = checksum(header + data)

    header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object

#向指定地址发送Ping消息
def doOnePing(destAddr, ID, sequence, timeout):
    icmp = socket.getprotobyname("icmp")

    # 创建原始套接字

    ########## Begin ##########
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
   
   
   ########## End ##########
    print(mySocket)
    sendOnePing(mySocket, ID, sequence, destAddr)

    mySocket.close()
    return 

#主函数Ping
def ping(host, timeout=1):
    
    # timeout=1指: 如果1秒内没从服务器返回，客户端认为Ping或Pong丢失。
    dest = socket.gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    
    #每秒向服务器发送一次Ping请求
    myID = os.getpid() & 0xFFFF  # 返回进程ID
    loss = 0
    for i in range(4):
        doOnePing(dest, myID, i, timeout)
    return


ping("127.0.0.1")