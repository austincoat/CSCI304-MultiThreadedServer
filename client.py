#The Client class is simply used to act as a client while our other server is running
#It sends out a HTTP request like a browser would, so I used
#The wireshark HTTP lab to get the structure of a header filed
#And use here to pull the html document I wrote and print it
#Out to check if it received the error code or was received properly

#import socket module
from socket import *
# In order to terminate the program
import sys
#sudo netstat -ap | grep :6202 to check if all sockets are  killed
serverName= sys.argv[1]
serverPort= sys.argv[2]
fileName = sys.argv[3]
# put variables for the servername(IP),
#and Server Port in the proper format for the header
hostPort = "%s:%s" %(serverName, serverPort)
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,int(serverPort)))
    #Makes the head array with all 'object' arrays with
    #corresponding information for the server we made to take in
    head = {
	"header" : "GET /%s HTTP/1.1" %(fileName),
	"Accept": "text/html",
	"Accept-Language": "en-us",
	"Host": hostPort,
    }
    #You NEED To split the header up into its own lines so that
    #when it enters the server it reads each section of the header line by line
    httpHead = "\r\n".join("%s:%s" %(item,head[item]) for item in head)
    clientSocket.send("%s\r\n\r\n" %(httpHead))
except IOError:
    sys.exit(1)
#It sends you a multi line respones that you must go through
# and save each part into the response variable so that it
#cant print properly without breaking a pipe.
response = ""
responseMessage=clientSocket.recv(1024)
while responseMessage:
	response += responseMessage
	responseMessage = clientSocket.recv(1024)
clientSocket.close()
print "Client Set To Inactive. . ."
#Then so you know if the client actually received the information due to a lack of the gui vv
print response
