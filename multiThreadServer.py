from socket import *
import sys
import threading
serverPort = 6202
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)

#Found use of this function in Python
def createThread(tSocket,trash):
    try:
        message = tSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket
        tSocket.send("HTTP/1.1 200 OK\r\n\r\n")
        #Send the content of the requested file to the client
        tSocket.sendall(outputdata)
        tSocket.send("\r\n".encode())
        tSocket.close()
    except IOError:
        #Let user know the file was not found with status code 404
        tSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
        tSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        #Close client socket
        tSocket.close()


while True:
    #Establish the connection
    print('Ready to serve')
    tSocket, trash = serverSocket.accept()
    try:
        threading.Thread(target=createThread,args=(tSocket, trash)).start()
    except IOError:
        print("Thread not active")

serverSocket.close()
sys.exit()
