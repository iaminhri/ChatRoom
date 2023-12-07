import socket
import sys
from termcolor import colored, cprint
import threading
from pwn import *

# dictionary for emotes with a key and value
emoticons = {
	"/me": "\U0001F600"
}

'''
receives text from the server and checks if the text is user? or not, 
if a new connection is created a text user? is forwarded and 
based on that clients userName is sent to the server, which then broadcasts to all other clients
'''

def recv_msg(serv_sock):
	# boolean for exiting condition

	while True:
		try:
			msg = serv_sock.recv(2048) # receives a encoded text			
			if not msg:
				break

			decoded_msg = b64d(msg).decode('utf-8') # decodes the base64

			if decoded_msg == "user?": # checks if decoded_msg contains the param user? if so then forwards the userName
				server.send(b64e(userName.encode('utf-8')).encode())
			else: # otherwise simply prints out the message sent from server
				sys.stdout.write(colored(decoded_msg + " \n", "blue"))
				sys.stdout.flush()
		except Exception as e: # prints if there is any exeception
			sys.stdout.write(colored(f"Error: {e}", "red"))
			sys.stdout.flush()
			serv_sock.close()
			break

# opens a socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# checks for command line arguments, it takes three parameter including client.py 
if len(sys.argv) == 3:
	ip = socket.gethostbyname(sys.argv[1])
	port = int(sys.argv[2])
else:
	print(colored("Invalid amount of arguments", "red"))
	print(colored("Syntex is client.py ip_address port_number", "green"))
	sys.exit()

# connects to server
server.connect((ip, port))

# prompts a user name
userName = input(colored("Enter Your Username: ", "yellow")).rstrip()


# this thread is executed everytime a text appears on the client side as well as helps with concurrent text send with concurrent execution of the recv_msg function
recv_thread = threading.Thread(target=recv_msg, args=(server,))
recv_thread.start()

try:
	while True:
		keyIn = input() # takes keyboard input // this is for a text a client wants to send to the other client
		msg = "@" + str(userName) + ">  " + keyIn # appends username and input
		encoded_msg = b64e(msg.encode('utf-8')) # encodes the message
		server.send(encoded_msg.encode()) # sends to the server
		sys.stdout.write(colored("<you>  "))
		sys.stdout.flush()
		if not keyIn:
			break 
except KeyboardInterrupt: # if user exits then that is forwarded to the server and broadcasted to other users
	msg = "/exit" 
	encoded_msg = b64e(msg.encode('utf-8')) # encodes msg 
	server.send(encoded_msg.encode()) # sends the encoded msg to the server
finally:
	server.close() # closes the socket connection
	recv_thread.join() # waits for the recv_thread to finish
	sys.exit() # exits system
