# python_chat_app
A simple client server application using socket programming in python


## Formating used for messages:
1. Sending message to a user named 'test'
    test:hi this is a test message
2. Sending a query to server
    * Cheking friend list
        * server_command:friend_list
    * Cheking friend requests
        * server_command:friend_requests
    * Sending friend request to a user named test
        * server_command:send_friend_request>test
    * Accepting a friend request from user name test
        * server_command:accept_friend_request>test
    * Checking online friends
        * server_command:online_friends
    * Logout of session
        * server_command:exit
3. Everyone can send message to server for that use the username 'server'
    note: server and server_command are diffrent, server_command is used for sending queries to server while server can be used for sending general messages
4. Server can send message to anyone

        

## CSV files and their roles:
1. user_info.csv : stores list of registered users and passwords
2. friend_requests.csv : stores pending friend requests of users
3. user_friends.csv : sotres friend lists of users



## Some features:
1. You can send message to only those users which are online and are in your friend list
2. You can send friend request to a user even if he/she is offline
3. Firend request can not be sent to a non-existing user
4. Can't create an account with same duplicate username
5. Can't create an account with name server or server_command(reserved for sending queries to server)
