#ICMPPing.py

import socket
import os
import struct
import time
import select

ICMP_ECHO_REQUEST = 8

#生成校验和
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

#发送一次Ping数据包
def sendOnePing(mySocket, ID, sequence, destAddr):
    # 头部构成： type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    ########## Begin ##########
    
    # 生成一个校验和为0的虚拟头部.
    # struct.pack() -- 将字符串信息封装成二进制数据
    header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    # 这里按理说应该是 时间戳:1577808000，但是答案直接就是 2020-1-1=2018
    data = struct.pack('!d', 2018)
    # 计算头部和数据的校验和
    myChecksum = checksum(header + data)

    header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    packet = header + data
    
    ########## End ##########
    
    print(packet)
    mySocket.sendto(packet, (destAddr, 1))  
   

#向指定地址发送Ping消息
def doOnePing(destAddr, ID, sequence, timeout):
    icmp = socket.getprotobyname("icmp")

    # 创建原始套接字
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
 
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
    myID = 0x1234  # 模拟发送者ID
    loss = 0
    for i in range(4):
        result = doOnePing(dest, myID, i, timeout)
    return

ping("127.0.0.1")