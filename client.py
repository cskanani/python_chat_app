import socket
import select 
import sys 

srv= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = str(sys.argv[1])
srv.connect((host,12345))
print("Connected to ",host)

try:
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
                #print('Users online\n')
                #while True:
                    #onl = srv.recv(1024).decode('utf-8')
                    #if(onl != '-1'):
                        #print(onl)
                    #else:
                        #break
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
                    print('Users online\n')
                    while True:
                        onl = srv.recv(1024).decode('utf-8')
                        if(onl != '-1'):
                            print(onl)
                        else:
                            break
                    break
                else:
                    print('Username already exist, try another username')
                
    msglbf = True
    while msglbf: 
        sockets_list = [sys.stdin, srv] 
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    
        for socks in read_sockets: 
            if socks == srv: 
                message = socks.recv(1024).decode('utf-8')
                if len(message) == 0:
                    msglbf = False
                    break
                print(message)
            else:
                message = sys.stdin.readline() 
                srv.send(bytes(message,'utf-8'))
except:
    srv.send(bytes('srv:close','utf-8'))
    srv.close()
