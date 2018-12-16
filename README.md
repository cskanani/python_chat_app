# python_chat_app
A simple client server application using socket programming in python


## Formating used for messages:
1. Sending message to a user named 'test'
    test:hi this is a test message
2. Sending a query to server
    * Cheking friend list
        srvc:fl
    * Cheking friend requests
        srvc:fr
    * Sending friend request to a user named test
        srvc:sfr>test
    * Accepting a friend request from user name test
        srvc:afr>test
    * Checking online friends
        srvc:ou
    * Logout of session
        srvc:exit
3. Everyone can send message to server for that use the username 'srv'
    note: srv and srvc are diffrent, srvc is used for sending queries to server while srv can be used for sending general messages
4. Server can also send message to anyone

        

## CSV files and their roles:
1. usrlst.csv : stores list of registered users and passwords
2. frlst.csv : stores pending friend requests of users
3. usrfr.csv : sotres friend lists of users



## Some features:
1. You can send message to only those users which are online and are in your friend list
2. You can send friend request to a user even if he/she is offline
3. Firend request can not be sent to a non-existing user
4. Can't create an account with same name as pre-existing user
5. Can't create an account with name srv(reserved for sending queries to server)
