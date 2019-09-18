from socket import *
import os,sys
HOST='127.0.0.1'
PORT=9999
ADDR = (HOST,PORT)


def main():
    sockfd = socket(AF_INET,SOCK_DGRAM)
    while True:
        name=input('请输入昵称')
        msg='L '+name
        sockfd.sendto(msg.encode(),ADDR)
        data,addr = sockfd.recvfrom(1024)
        if data==b'OK':
            print('您已经进入聊天室')
            break
        else:
            print(data.decode())
    pid=os.fork()
    if pid<0:
        sys.exit('Error!')
    elif pid==0:
        send_msg(sockfd,name)
    else:
        recv_msg(sockfd)

def send_msg(sockfd,name):
    while True:
        try:
            msg=input('>>>')
        except KeyboardInterrupt:
            msg='quit'
        if msg.strip()=='quit':
            msg='Q %s'%name
            sockfd.sendto(msg.encode(),ADDR)
            sys.exit('您已退出聊天室')
        temp='C %s %s'%(name,msg)
        sockfd.sendto(temp.encode(),ADDR)


def recv_msg(sockfd):
    while True:
        data,addr=sockfd.recvfrom(1024)
        if data.decode()=='EXIT':
            sys.exit()
        print(data.decode()+'\n>>>',end='')



if __name__ == '__main__':
    main()




