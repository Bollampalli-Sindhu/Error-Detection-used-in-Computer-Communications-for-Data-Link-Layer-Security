import socket
import sys
import threading  
import numpy as np 
import ast
from threading import Thread

MSG_SIZE = 1024
port = 8015
key = "1011"
A_inv = np.array([[1,0,1],[4,4,3],[-4,-3,-3]]) 

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

def ascii_to_string(array):
    n=array.shape[1]
    array=(array.T).reshape(1,n*3).tolist()[0]
    res = "" 
    for val in array: 
        res = res + chr(val)
    return res.strip()

def validate_msg(msg):
    enc_data,E=ast.literal_eval(msg)
    n = int(len(enc_data)/3)
    
    enc_data= np.array(enc_data).reshape(n,3).T
    dec_data = np.dot(A_inv,enc_data)
    
    data= ascii_to_string(dec_data)
    E1 = CRC(binary_form(data),key)
    if(E == E1):
        return data
    else:
        return -1
    

def handle_connection(cli_sd,addr):
    while True:
        msg=cli_sd.recv(MSG_SIZE).decode('utf-8')  
        msg= validate_msg(msg)
        if msg=="exit":
            break
        if msg == -1:
            print("Recieved message is corrupted")
            cli_sd.send("failed".encode())
        else:
            cli_sd.send("success".encode())
            print("Message from",addr[1]," : ",msg)
    cli_sd.close()

soc_id=socket.socket()
soc_id.bind(('', port))
soc_id.listen(5)
threads = [None] * 5
i=0
while True:
    cli_sd, addr = soc_id.accept()
    threads[i] = Thread(target=handle_connection,args=(cli_sd,addr))
    threads[i].start()
    i+=1
    # handle_connection(cli_sd)  
for j in range(len(threads)):
    threads[j].join()