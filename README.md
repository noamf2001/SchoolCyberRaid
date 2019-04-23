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
			
4:

	get file:
		main server to all data server: file name (with username at start), port to send parts to
		data server to main server: file parts (do not send if it does not have\send a few parts)
	msg parameters:
		main server to data server:
			len of file name + $ + file name + port (5 digits - max port 65535)
		data server to main server:
			len of file part name + $ + file part name + file data (set size)


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
			
4:

	get file:
		client to server: file name(with username at start)
		server to client: file data ("" if could not retrieve)
	msg parameters:
		client to server:
			len of file name + $ + file name
		server to client:
			len of file data (could be 0) + $ + file data
