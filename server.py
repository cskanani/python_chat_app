import socket
import atexit
from _thread import *
from _thread import *
from tkinter import *
from tkinter import scrolledtext
import sys

server_socket = socket.socket()
host = sys.argv[1]
server_socket.bind((host, 1234))
server_socket.listen(10)

friend_requests_file = open('friend_requests.csv', 'r')
friend_requests = {}
for line in friend_requests_file.readlines():
    username, request_list = line.strip('\n').split(':')
    friend_requests.update({username: request_list.split(',')})
friend_requests_file.close()

user_info_file = open('user_info.csv', 'r')
user_info = {}
for line in user_info_file.readlines():
    usrname, password = line.strip('\n').split(',')
    user_info.update({username: password})
user_info_file.close()

user_friends_file = open('user_friends.csv', 'r')
user_friends = {}
for line in user_friends_file.readlines():
    username, friend_list = line.strip('\n').split(':')
    user_friends.update({username: friend_list.split(',')})
user_friends_file.close()

online_users = []
user_to_socket = {}

def main(text_entry, text_box):
    def connect(client_socket, address, text_entry, text_box):
        print("Connected with ", address)
        # authenticate client
        while True:
            choice = int(client_socket.recv(1024).decode('utf-8'))
            client_username, password = client_socket.recv(1024).decode('utf-8').split(',')
            if(choice == 1):
                if(client_username in user_info and user_info[client_username] == password):
                    client_socket.send(bytes('1', 'utf-8'))
                    online_users.append(client_username)
                    user_to_socket.update({client_username: client_socket})
                    break
                else:
                    client_socket.send(bytes('0', 'utf-8'))
                    
            elif(choice == 2):
                if(client_username in ['server', 'server_command'] or client_username in user_info):
                    client_socket.send(bytes('0', 'utf-8'))
                else:
                    user_info.update({client_username: password})
                    client_socket.send(bytes('1', 'utf-8'))
                    online_users.append(client_username)
                    user_to_socket.update({client_username: client_socket})
                    break
        
        #loop for getting messages from client and sending response
        while True:
            username, message = client_socket.recv(1024).decode('utf-8').split(':', 1)
            if(username == 'server_command'):                
                if(message == 'exit'):
                    online_users.remove(client_username)
                    del user_to_socket[client_username]
                    client_socket.send(bytes('You are now offline please close the window', 'utf-8'))
                    client_socket.close()
                    break
                elif(message == 'online_friends'):
                    if(client_username in user_friends):
                        for user in online_users:
                            if(user in user_friends[client_username]):
                                client_socket.send(bytes(user, 'utf-8'))
                    else:
                        client_socket.send(bytes('You don\'t have any friends', 'utf-8'))
                elif(message == 'friend_requests'):
                    if(client_username in friend_requests):
                        for user in friend_requests[client_username]:
                            client_socket.send(bytes(user, 'utf-8'))
                    else:
                        client_socket.send(bytes('You have no friend request', 'utf-8'))
                elif(message == 'friend_list'):
                    if(client_username in user_friends):
                        for user in user_friends[client_username]:
                            client_socket.send(bytes(user, 'utf-8'))
                    else:
                        client_socket.send(bytes('You don\'t have any friends.', 'utf-8'))
                elif(message.split('>')[0] == 'send_friend_request'):
                    other_user = message.split('>')[1]
                    if(client_username in user_friends and
                    other_user in user_friends[client_username]):
                        client_socket.send(bytes('You are already friend with {}'
                        .format(other_user), 'utf-8'))
                    else:
                        if(other_user in user_info):
                            if(other_user in friend_requests):
                                friend_requests[other_user].append(client_username)
                            else:
                                friend_requests.update({other_user: [client_username]})
                            client_socket.send(bytes('Friend request sent to {}'
                            .format(other_user), 'utf-8'))
                        else:
                            client_socket.send(bytes('User does not exist plese enter a valid username.',
                             'utf-8'))
                elif(message.split('>')[0] == 'accept_friend_request'):
                    other_user = message.split('>')[1]
                    if(client_username in friend_requests and
                    other_user in friend_requests[client_username]):
                        friend_requests[client_username].remove(other_user)
                        if(client_username in user_friends):
                            user_friends[client_username].append(other_user)
                        else:
                            user_friends.update({client_username:[other_user]})
                        if(other_user in user_friends):
                            user_friends[other_user].append(client_username)
                        else:
                            user_friends.update({other_user:[client_username]})
                        client_socket.send(bytes('You are now friend with {}'
                        .format(other_user), 'utf-8'))
                    else:
                        client_socket.send(bytes('You don\'t have friend request from {}'
                        .format(other_user), 'utf-8'))
            elif(username == 'server'):
                text_box.insert(INSERT, client_username + '_m : ' + message + '\n')
            else:
                if(client_username in user_friends and username in user_friends[client_username]):
                    if(username in online_users):
                        user_to_socket[username].send(bytes(client_username + '_m : ' + message, 'utf-8'))
                    else:
                        client_socket.send(bytes('{} is not online, message is not delievered.'
                        .format(username), 'utf-8'))
                else:
                    client_socket.send(bytes('You are not friend with {}, message is not delievered.'
                    .format(username), 'utf-8'))
                    
                
    while True:
        client_socket, address = server_socket.accept()
        start_new_thread(connect, (client_socket, address, text_entry, text_box))


def send(text_entry, text_box):
    message = text_entry.get()
    text_box.insert(INSERT, message + '\n')
    username, message = message.split(':')
    if(username in online_users):
        user_to_socket[username].send(bytes('server_m : ' + message, 'utf-8'))
    else:
        text_box.insert(INSERT, '{} is not online, message is not delievered.'.format(username) + '\n')
    text_entry.delete(0, 'end')

root = Tk()
root.resizable(0, 0)
root.title('Server Chat Window')
root.bind("<Return>", send)
text_box = scrolledtext.ScrolledText(root)
text_box.grid(column = 0, row = 0, columnspan = 2)
text_entry = Entry(root, width = 65)
text_entry.grid(column = 0, row = 1)
send_button = Button(root, text = "Send", command = lambda: send(text_entry, text_box), width = 10)
send_button.grid(column = 1, row = 1)

start_new_thread(main, (text_entry, text_box))
root.mainloop()



print('handling exit')
friend_requests_file = open('friend_requests.csv', 'w')
friend_requests_file.truncate()
for user in friend_requests:
    if(friend_requests[user]):
        friend_requests_file.write(user + ':' + ','.join(friend_requests[user]) + '\n')
friend_requests_file.close()

user_info_file = open('user_info.csv', 'w')
user_info_file.truncate()
for user in user_info:
    if(len(user)>3):
        user_info_file.write(user + ',' + user_info[user] + '\n')
user_info_file.close()

user_friends_file = open('user_friends.csv', 'w')
user_friends_file.truncate()
for user in user_friends:
    if(user_friends[user]):
        user_friends_file.write(user + ':' + ','.join(user_friends[user]) + '\n')
user_friends_file.close()
server_socket.close()
