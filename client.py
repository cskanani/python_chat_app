import socket
import select 
import sys 
from _thread import *
from tkinter import *
from tkinter import scrolledtext

server = socket.socket()
host = str(sys.argv[1])
server.connect((host, 1234))
print("Connected to ", host)

# login or register to system
while True:
    print('1. Login\n2. Register\n3. Quit')
    choice = int(input('Enter your choice : '))
    if(choice == 1):
        server.send(bytes('1', 'utf-8'))
        username = input("Username : ")
        password = input("Password : ")
        server.send(bytes(username + ',' + password, 'utf-8'))
        server_reply = int(server.recv(1024).decode('utf-8'))
        if(server_reply):
            print('Authentication successful\n')
            break
        else:
            print('Username or Password was incorrect, try again')
        
    elif(choice == 2):
        username = input("Username : ")
        password = input("Password : ")
        password_confirm = input("Confirm Password : ")
        if(password ! = password_confirm):
            print('Passwords dont match, try again')
        else:
            server.send(bytes('2', 'utf-8'))
            server.send(bytes(username + ',' + password, 'utf-8'))
            server_reply = int(server.recv(1024).decode('utf-8'))
            if(server_reply):
                print('Registration successful\n')
                break
            else:
                print('Username already exist, try another username')
            
# get messages from server and append to text box
def get_message(server, text_box):
    while True:
        message = server.recv(1024).decode('utf-8')
        if not(message):
            server.close()
            break
        text_box.insert(INSERT, message + '\n')

# send message to server, also adds message text to text box
def send(text_entry, text_box):
    message = text_entry.get()
    text_box.insert(INSERT, message + '\n')
    server.send(bytes(message, 'utf-8'))
    text_entry.delete(0, 'end')

root = Tk()
root.resizable(0, 0)
root.title(username + ' Chat Window')
root.bind("<Return>", send)
text_box = scrolledtext.ScrolledText(root)
text_box.grid(column = 0, row = 0, columnspan = 2)
text_entry = Entry(root, width = 65)
text_entry.grid(column = 0, row = 1)
send_button = Button(root, text = "Send", command = lambda: send(text_entry, text_box), width = 10)
send_button.grid(column = 1, row = 1)

start_new_thread(get_message, (server, text_box))
root.mainloop()
