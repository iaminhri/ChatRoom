Install the requirements file

For Windows: 
try running the bash file first, if bash not enabled on windows then following is required,

download the file if you don't have pip
https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip --version -> to check pip version

# note: if pip is intalled above is not required.

Open the requirements.txt run the provided commands

For linux:
run ./install_me.sh (easy)

this will install pip if it doesn't exist, termcolor and pwntools

#note: i used pwntools for base64 encoding and decoding.

Server and Client program can launched in one PC

Three terminals needed for that.

1st cmd: python3 server.py localhost 7777

2nd cmd: python3 client.py localhost 7777

3rd cmd: python3 client.py localhost 7777

# note: it is possible to change to a different ip address.

For example, 

Computer0: python3 server.py 192.168.2.4 7777

Computer1: python3 client.py 192.168.2.4 7777

Computer0: python3 client.py 192.168.2.4 7777

# note: all the computer has to be under one network, or probably a static IP(Couldn't check).

# note: lastly to finish it off, if multiple instances of clients were to run repeatedly, use the following command to kill all process regarding this client server program
killall -9 python3

I hope I didn't miss anything. Thank you for your time :D.