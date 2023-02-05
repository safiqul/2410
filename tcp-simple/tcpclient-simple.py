from socket import *
def main():
	message = "Hello world"
	client_sd = socket(AF_INET,SOCK_STREAM) 
	server_ip = '127.0.0.1' 
	port = 12000  	

	#connect to the server 
	client_sd.connect((server_ip, port)) 

	#Send data 
	client_sd.send(message.encode());

	#Read data from the socket
	received_line = client_sd.recv(1024).decode()
	#print
	print(received_line) 
	#closing the connection
	client_sd.close()

if __name__=='__main__':
	main()
