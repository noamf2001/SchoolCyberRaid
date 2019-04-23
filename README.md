# SchoolCyberRaid
Raid protocol:

file name: 
	
	username + $ + filename
	
file part:
	
	filename_part + _ + number + _ + if it is a parity file - the other part number, else -1
	
msg:

	len of msg + $ + msg type + $ + msg parameters

msg parameters is determine by msg type

msg type

-1: 
	socket crash

0:  

	key exchange
		client to server: asymmetric key
		server to client: symmetric key
	msg parameters:
		key

data server - main server protocol:

3: 

	upload file:
    		main server to data server: file name(with username at start), file data
    		data server to main server: None
    	msg parameters:
		main server to data server:
			file name
			file data
		data server to main server:
			None


client - main server protocol:
        
1:

	sign in:
		client to server: username, password(after hash)
        	server to client: boolean if success
	msg parameters:
        	client to server: 
            		len of username + $ + username + len of password + $ + password
		server to client:
            		0 - False
            		1 - True
			
2:

	sign in:
        	client to server: username, password(after hash)
        	server to client: boolean if success
	msg parameters:
        	client to server: 
            		len of username + $ + username + len of password + $ + password
		server to client:
            		0 - False
            		1 - True
3:

	upload file:
        	client to server: file name (with username at start), file data
        	server to client: boolean if success
	msg parameters:
        	client to server:
            		len of file + $ + file name + len of file data + $ + file data
		server to client:
        		0 - False
         		1 - True
