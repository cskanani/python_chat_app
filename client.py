import socket
import select 
import sys 
from _thread import *
from tkinter import *
from tkinter import scrolledtext

srv= socket.socket()
host = str(sys.argv[1])
srv.connect((host,1234))
print("Connected to ",host)


while True:
    print('1. Login\n2. Register\n3. Quit')
    ch = int(input('Enter your choice : '))
    if(ch == 1):
        srv.send(bytes('1','utf-8'))
        usrn = input("Username : ")
        pswd = input("Password : ")
        srv.send(bytes(usrn+','+pswd,'utf-8'))
        x = int(srv.recv(1024).decode('utf-8'))
        if(x):
            print('Authentication successful\n')
            break
        else:
            print('Username or Password was incorrect, try again')
        
    elif(ch == 2):
        usrn = input("Username : ")
        pswd1 = input("Password : ")
        pswd2 = input("Confirm Password : ")
        if(pswd1 != pswd2):
            print('Passwords dont match, try again')
        else:
            srv.send(bytes('2','utf-8'))
            srv.send(bytes(usrn+','+pswd1,'utf-8'))
            x = int(srv.recv(1024).decode('utf-8'))
            if(x):
                print('Registration successful\n')
                break
            else:
                print('Username already exist, try another username')
            
def recv():
    global srv
    while True:
        msg = srv.recv(1024).decode('utf-8')
        if not(msg):
            srv.close()
            break
        txt.insert(INSERT,msg+'\n')

def send(event):
    global ent
    msg = ent.get()
    txt.insert(INSERT,msg+'\n')
    srv.send(bytes(msg,'utf-8'))
    ent.delete(0,'end')

root = Tk()
root.resizable(0,0)
root.title(usrn+' Chat Window')
root.bind("<Return>", send)
txt = scrolledtext.ScrolledText(root)
txt.grid(column=0,row=0,columnspan = 2)
ent = Entry(root,width=65)
ent.grid(column=0, row=1)
btn = Button(root, text="Send", command=send,width=10)
btn.grid(column=1, row=1)

start_new_thread(recv,())
root.mainloop()
