# SchoolCyberRaid
Raid protocol:

file name: 
	
	username + $ + filename
	in server + data sesrver:
		filename = filename without ending + _ + ending + .gz
	
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
			len of file name + $ + file name + port
		data server to main server:
			len of file part name + $ + file part name + file data (set size)

5:

	delete file:
		main server to all data server: file name (with username at start)
		data server to main server: None
	msg parameters:
		main server to data server:
			file name
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
			
4:

	get file:
		client to server: file name(with username at start)
		server to client: file data ("" if could not retrieve)
	msg parameters:
		client to server:
			len of file name + $ + file name
		server to client:
			len of file data (could be 0) + $ + file data

5:

	delete file:
		client to server: file name(with username at start)
		server to client: None
	msg parameters:
		client to server:
			len of file name + $ + file name
		server to client:
			None

6:

	get file list:
		client to server: None
		server to client: list of the files names
	msg parameters:
		client to server:
			""
		server to client:
			len of file 1 name + $ + file 1 name + len of file 2 name + $ + file 2 name
			
