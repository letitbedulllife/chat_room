'''
    chat room
    env:python3.6
    socket udp & fork exc

'''


import os
from socket import *

HOST='0.0.0.0'
PORT=9999
sockfd_addr=(HOST,PORT)

user_data=[]


def controller_data(sockfd):
    while True:
        msg=input('请输入管理员消息：')
        msg='C 管理员 '+msg
        sockfd.sendto(msg.encode(),sockfd_addr)

def do_quit(sockfd, name):
    msg='\n%s 退出了群聊'%name
    for item in user_data:
        if item[0]==name:
            sockfd.sendto(b'EXIT',item[1])
        else:
            sockfd.sendto(msg.encode(),item[1])
    for item in user_data:
        if item[0]==name:
            user_data.remove(item)

def do_chat(sockfd,name,text):
    msg='\n%s : %s'%(name,text)
    for i in user_data:
        if name!=i[0]:
            sockfd.sendto(msg.encode(),i[1])

def do_login(sockfd,name,addr):
    for item in user_data:
        if name == item[0]:
            sockfd.sendto('用户名已存在'.encode(),addr)
            return
    else:
        sockfd.sendto(b'OK',addr)
    msg='欢迎%s加入群聊'%name
    for item in user_data:
        sockfd.sendto(msg.encode(),item[1])
    user_data.append((name,addr))

def receive_data(sockfd):
    while True:
        data, addr =sockfd.recvfrom(1024)
        temp=data.decode().split(' ',2)
        if temp[0]=='L':
            do_login(sockfd,temp[1],addr)
        elif temp[0]=='C':
            do_chat(sockfd,temp[1],temp[2])
        elif temp[0]=='Q':
            do_quit(sockfd,temp[1])

def main():
    sockfd =socket(AF_INET,SOCK_DGRAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(sockfd_addr)
    pid = os.fork()
    if pid==0:
        receive_data(sockfd)
    else:
        controller_data(sockfd)

if __name__ == '__main__':
    main()













