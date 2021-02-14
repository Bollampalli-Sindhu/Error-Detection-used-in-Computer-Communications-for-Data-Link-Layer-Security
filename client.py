import socket             
import sys
import threading
import numpy as np 
# from Crypto.Cipher import DES3
# from Crypto.Random import get_random_bytes
# from random import randint
# import hashlib

MSG_SIZE=1024
port=8015
key ="1011"
A = np.array([[-3,-3,-4],[0,1,1],[4,3,4]])

if len(sys.argv) >1:
    port=int(sys.argv[1])

def XOR(a,b):
    res=""
    for i in range(len(a)):
        if a[i]==b[i]:
            res+="0"
        else:
            res+="1"
    return res[1:]

def binary_div(divident,divisor):
    n=len(divisor)
    n1=len(divident)
    val=divident[0:n]
    for i in range(n1-n):
        if val[0]=='1':
            val=XOR(divisor,val)+divident[n+i]
        else:
            val=val[1:]+divident[n+i]
    
    val=XOR(divisor,val) if val[0]=='1' else val[1:]

    return val

def CRC(data,key):
    n=len(key)
    new_data=data+'0'*(n-1)
    syn = binary_div(new_data,key)
    return data+syn

def binary_form(data):
    return ''.join(format(ord(i), 'b') for i in data)

def convert_vector(msg):
    res=[]
    for ele in msg: 
        res.extend(ord(num) for num in ele)
    res = np.array(res+[32]*((3-len(res))%3))
    n = int(len(res)/3)
    res= res.reshape(n,3).T
    return res

def flatten(data):
    n=data.shape[1]
    data=((data.T).reshape(1,n*3)).tolist()[0]
    return data

def encrypt(msg):
    E=CRC(binary_form(msg),key)
    p=convert_vector(msg)
    enc_data = np.dot(A,p)
    enc_data=flatten(enc_data)
    msg = str([enc_data,E]) 
    return msg

soc_id=socket.socket()
soc_id.connect(("127.0.0.1",port))

while True:
    msg=input().strip()
    enc_data=encrypt(msg)
    soc_id.send(enc_data.encode())
    if msg=="exit":
        break
    msg=soc_id.recv(MSG_SIZE).decode('utf-8')
    if msg == "success":
        print("Message sent successfully\n")
    else:
        print("The message is corrupted in the network")
soc_id.close()