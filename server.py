
import socket
import sys
from termcolor import colored
import threading
from pwn import *


# handles new connections and messages from the clients, recieves texts from clients and broadcasts to all the other users
def client_handler(conn, ip):
	# Basic greeting on the chat server, encodes in base64 and encodes the inner string using latin-1
	str = "Welcome to the chatroom\ntype '/exit' to close the connection.\n/me to send a happy emoticon"
	str_encode = b64e(str.encode('utf-8'))

	#sends a byte stream through the socket.
	conn.send(str_encode.encode())

	while True:
		try: 
			msg = conn.recv(2048) # recieves data 

			decoded_msg = b64d(msg).decode('utf-8') # decodes the base64 data that was recieved via socket
			if "/exit" in decoded_msg: # exits if /exit is written on chat
				indx = clients.index(conn) # finds the index of the current client
				remove(conn) # calls remove function to remove the connection
				user = users[indx] # client is saved in user variable
				removeClientMsg = "/exit> " + user + " has left the chatroom" # concatenates the username and broadcasts to all the other clients
				broadcastMsg(removeClientMsg, conn)
				users.remove(user) # lastly removes the user as well
				break
			elif decoded_msg and "/me" in decoded_msg: # this section checks if there /me in the text and replaces it with a happy emoticon
				decoded_msg = decoded_msg.replace("/me", "\U0001F600") # replace /me with unicode of the happy emoticon
				sys.stdout.write(colored("\n<" + ip[0] + decoded_msg, "blue")) # prints on the server side
				send_msg = "<" + ip[0] + decoded_msg 
				broadcastMsg(send_msg, conn) # sends the message to all the other clients
				sys.stdout.flush() # flushes the system buffer
			elif decoded_msg: # if the simple text then forwards it to other clients
				sys.stdout.write(colored("<" + ip[0] + decoded_msg, "blue"))
				send_msg = "<" + ip[0] + decoded_msg
				broadcastMsg(send_msg, conn)
				sys.stdout.flush()
		except:
			continue

# sends broadcast message, for a single client's message, iterates over all the client connected to socket and forwards messages to all of them
def broadcastMsg(msg, conn): # this function is called inside client handler function
	msg = b64e(msg.encode('utf-8'))
	for client in clients:
		if client != conn:
			try:
				client.send(msg.encode('utf-8'))
			except:
				client.close()
				remove(client)

def remove(conn): # remove a client
	if conn in clients:
		clients.remove(conn)
		conn.close()

# opens IPv6 client connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # sets socket options, sockets reusable

# arguments for the script to run, script has 3 arguments, if not throws an error
if len(sys.argv) == 3:
	ip_addr = socket.gethostbyname(sys.argv[1])
	port = int(sys.argv[2])
else:
	print(colored("Invalid amount of arguments", "red"))
	print(colored("Syntex is client.py ip_address port_number", "green"))

# binds the ip and the port passed through the command args
sock.bind((ip_addr, port))

sock.listen(10)

clients = []
users = []

# main function
try:
	while True:
		conn, ip = sock.accept()
		clients.append(conn) # appends new client connection

		print(colored(ip[0] + " connected\n", "yellow")) # prints @ip connected on the server side

		# user? text is sent to the client. base64 encoded text is sent.
		user_msg = b64e("user?".encode('utf-8')) 
		conn.send(user_msg.encode())

		# user recieves some data
		user = conn.recv(2048)
		user = b64d(user).decode('utf-8') # decodes it
		users.append(user) # A user is appended with users list
		broadcastMsg(colored(f'\n<{user}> has joined the chat room\n', "yellow"), conn) # broadcasts the incoming new user

		str2 = "\nYou are now connected!\n" # sends the following message
		send_msg = b64e(str2.encode('utf-8'))
		conn.send(send_msg.encode())

		try:
			# a concurrent thread is running for the client handler, for each connection a new thread is generated
			threading.Thread(target=client_handler, args=(conn, ip)).start()
		except KeyboardInterrupt:
			print("Keyboard Interrupted: Exiting server...")
			sys.exit()

	sock.close()
	conn.close() # connection closed
except KeyboardInterrupt:
	print("Keyboard Interrupted: Exiting Server")
	sys.exit()