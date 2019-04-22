# SchoolCyberRaid
Raid
client server protocol:



msg:
len of msg
$
msg type
$
msg parameters

msg parameters is organize by msg type

msg type:
-1: socket crash
0:  key exchange,
        client to server: asymmetric key
        server to client: symmetric key
    msg parameters:
        just the key itself
        
        
1:  sign up:
        client to server: username, password (after hash)
        server to client: boolean if success
    msg parameters:
        client to server: 
            len of username
            $
            username
            
            len of password
            $
            password
        server to client:
            0 - False
            1 - True
            
2:  sign in:
        client to server: username, password(after hash)
        server to client: boolean if success
    msg parameters:
        client to server: 
            len of username
            $
            username
            
            len of password
            $
            password
        server to client:
            0 - False
            1 - True
3:  upload file:
        client to server: file name, file data
        server to client: boolean if success
    msg parameters:
        client to server:
            len of file
            $
            file name
            
            len of file data
            $
            file data
        server to client:
            0 - False
            1 - True
