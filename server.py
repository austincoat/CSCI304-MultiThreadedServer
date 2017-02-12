#import socket module
from socket import *
# In order to terminate the program
import sys
#sudo netstat -ap | grep :6201 to check if all sockets are  killed
serverPort = 6201
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket, only expecting html
        connectionSocket.send('HTTP/1.1 200 OK\r\n Content-Type: text/html\r\n\r\n')
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        #Let user know the file was not found with status code 404
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        #Close client socket
        connectionSocket.close()
        print("Socket Closed.")
serverSocket.close()
#Terminate the program after sending the corresponding data
sys.exit()
