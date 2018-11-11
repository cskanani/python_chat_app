import socket
import atexit
from _thread import *
from _thread import *
from tkinter import *
from tkinter import scrolledtext
import sys

s= socket.socket()
host = sys.argv[1]
s.bind((host, 1234))
s.listen(10)

frlst = open('frlst.csv','r')
frdict = {}
for x in frlst.readlines():
    usr,req = x.strip('\n').split(':')
    frdict.update({usr:req.split(',')})
frlst.close()

usrlst = open('usrlst.csv','r')
usrdict = {}
for x in usrlst.readlines():
    usr,pas = x.strip('\n').split(',')
    usrdict.update({usr:pas})
usrlst.close()

usrfr = open('usrfr.csv','r')
usrfrdict = {}
for x in usrfr.readlines():
    usr,req = x.strip('\n').split(':')
    usrfrdict.update({usr:req.split(',')})
usrfr.close()

coul = []
usrn2sc = {}

def main():
    def con(c,addr):
        print("Connected with ",addr)
        mlbf = True
        #loop for setting connection
        while True:
            ch = int(c.recv(1024).decode('utf-8'))
            cusrn,pas = c.recv(1024).decode('utf-8').split(',')
            if(ch == 1):
                if(cusrn in usrdict and usrdict[cusrn] == pas):
                    c.send(bytes('1','utf-8'))
                    coul.append(cusrn)
                    usrn2sc.update({cusrn:c})
                    break
                else:
                    c.send(bytes('0','utf-8'))
                    
            elif(ch == 2):
                if(cusrn in ['srv','srvc'] or cusrn in usrdict):
                    c.send(bytes('0','utf-8'))
                else:
                    usrdict.update({cusrn:pas})
                    c.send(bytes('1','utf-8'))
                    coul.append(cusrn)
                    usrn2sc.update({cusrn:c})
                    break
        
        #loop for getting messages from client and sending response
        while True:
            usrn,msg = c.recv(1024).decode('utf-8').split(':',1)
            if(usrn == 'srvc'):                
                if(msg == 'exit'):
                    coul.remove(cusrn)
                    del usrn2sc[cusrn]
                    c.send(bytes('You are now offline please close the window','utf-8'))
                    c.close()
                    break
                elif(msg == 'ou'):
                    if(cusrn in usrfrdict):
                        for x in coul:
                            if(x in usrfrdict[cusrn]):
                                c.send(bytes(x,'utf-8'))
                    else:
                        c.send(bytes('You don\'t have any friends','utf-8'))
                elif(msg == 'fr'):
                    if(cusrn in frdict):
                        for x in frdict[cusrn]:
                            c.send(bytes(x,'utf-8'))
                    else:
                        c.send(bytes('You have no friend request','utf-8'))
                elif(msg == 'fl'):
                    if(cusrn in usrfrdict):
                        for x in usrfrdict[cusrn]:
                            c.send(bytes(x,'utf-8'))
                    else:
                        c.send(bytes('You don\'t have any friends.','utf-8'))
                elif(msg[:3] == 'sfr'):
                    print(msg.split('>')[1])
                    if(cusrn in usrfrdict and msg.split('>')[1] in usrfrdict[cusrn]):
                        c.send(bytes('You are already friend with {}'.format(msg.split('>')[1]),'utf-8'))
                    else:
                        if(msg.split('>')[1] in usrdict):
                            if(msg.split('>')[1] in frdict):
                                frdict[msg.split('>')[1]].append(cusrn)
                            else:
                                frdict.update({msg.split('>')[1]: [cusrn]})
                            c.send(bytes('Friend request sent to {}'.format(msg.split('>')[1]),'utf-8'))
                        else:
                            c.send(bytes('User does not exist plese enter a valid username.','utf-8'))
                elif(msg[:3] == 'afr'):
                    if(cusrn in frdict and msg.split('>')[1] in frdict[cusrn]):
                        frdict[cusrn].remove(msg.split('>')[1])
                        if(cusrn in usrfrdict):
                            usrfrdict[cusrn].append(msg.split('>')[1])
                        else:
                            usrfrdict.update({cusrn:[msg.split('>')[1]]})
                        if(msg.split('>')[1] in usrfrdict):
                            usrfrdict[msg.split('>')[1]].append(cusrn)
                        else:
                            usrfrdict.update({msg.split('>')[1]:[cusrn]})
                        c.send(bytes('You are now friend with {}'.format(msg.split('>')[1]),'utf-8'))
                    else:
                        c.send(bytes('You don\'t have friend request from {}'.format(msg.split('>')[1]),'utf-8'))
            elif(usrn == 'srv'):
                txt.insert(INSERT,cusrn+'_m : '+msg+'\n')
            else:
                if(cusrn in usrfrdict and usrn in usrfrdict[cusrn]):
                    if(usrn in coul):
                        usrn2sc[usrn].send(bytes(cusrn+'_m : '+msg,'utf-8'))
                    else:
                        c.send(bytes('{} is not online, message is not delievered.'.format(usrn),'utf-8'))
                else:
                    c.send(bytes('You are not friend with {}, message is not delievered.'.format(usrn),'utf-8'))
                    
                
    while True:
        c,addr = s.accept()
        start_new_thread(con,(c,addr))


def send(event):
    global ent
    msg = ent.get()
    txt.insert(INSERT,msg+'\n')
    usrn,msg = msg.split(':')
    if(usrn in coul):
        usrn2sc[usrn].send(bytes('srv_m : '+msg,'utf-8'))
    else:
        txt.insert(INSERT,'{} is not online, message is not delievered.'.format(usrn)+'\n')
        #c.send(bytes('{} is not online, message is not delievered.'.format(usrn),'utf-8'))
    ent.delete(0,'end')

root = Tk()
root.resizable(0,0)
root.title('Server Chat Window')
root.bind("<Return>", send)
txt = scrolledtext.ScrolledText(root)
txt.grid(column=0,row=0,columnspan = 2)
ent = Entry(root,width=65)
ent.grid(column=0, row=1)
btn = Button(root, text="Send", command=send,width=10)
btn.grid(column=1, row=1)

start_new_thread(main,())
root.mainloop()



print('handling exit')
frlst = open('frlst.csv','w')
frlst.truncate()
for x in frdict:
    if(frdict[x]):
        frlst.write(x+':'+','.join(frdict[x])+'\n')
frlst.close()

usrlst = open('usrlst.csv','w')
usrlst.truncate()
for x in usrdict:
    if(len(x)>3):
        usrlst.write(x+','+usrdict[x]+'\n')
usrlst.close()

usrfr = open('usrfr.csv','w')
usrfr.truncate()
for x in usrfrdict:
    if(usrfrdict[x]):
        usrfr.write(x+':'+','.join(usrfrdict[x])+'\n')
usrfr.close()
s.close()
