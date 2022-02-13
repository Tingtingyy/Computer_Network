# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 10:12:32 2021

@author: hp
"""


from socket import *
serverPort = 9090
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
mailResponse = ''


def SMTPServer(connectionSocket):              
    # reply 220 SMTP server ready
    reply = '220 Alice Email server is ready to receive\r\n'
    connectionSocket.send(reply.encode())
    
    # reply HELO command
    data = connectionSocket.recv(1024).decode()            
    if data[:4] == 'HELO':
        print (data)
        heloReply = '250 Hello, pleased to meet you\r\n'
        connectionSocket.send(heloReply.encode())
    
    # reply MAIL FROM command
    data = connectionSocket.recv(1024).decode()   
    if data[:9] == 'MAIL FROM':
        print (data)
        s1 = data.split('<')[1]
        fromClient = s1.split('>')[0]
        mfromReply = '250 Alice Sender ok \r\n'
        connectionSocket.send(mfromReply.encode())

    # reply RCPT TO command
    data = connectionSocket.recv(1024).decode()     
    if data[:7] == 'RCPT TO':
        print (data)
        s1 = data.split('<')[1]
        rcptServer = s1.split('>')[0]
        rcptToReply = '250 Bob Mail Server Recipient ok\r\n'
        connectionSocket.send(rcptToReply.encode())

    # reply DATA command
    data = connectionSocket.recv(1024).decode()
    if data[:4] == 'DATA':
        print (data)
        dataReply = '354 Enter mail, end with "." on a line by itself\r\n'
        connectionSocket.send(dataReply.encode())

    # receive mail data
    msgBox = []
    endmsg = "\r\n.\r\n"
    while True:
        data = connectionSocket.recv(1024).decode()
        if endmsg in data:
            msgBox.append(data[:data.find(endmsg)])
            break
        msgBox.append(data)
        if len(msgBox)>1:
            Lasttwo = msgBox[-2]+msgBox[-1]
            if endmsg in Lasttwo:
                msgBox[-2] = Lasttwo[:Lasttwo.find(endmsg)]
                msgBox.pop()
                break          
    msg = ''.join(msgBox)
    print(msg+endmsg)
    endReply = '250 Message accepted for delivery\r\n'
    connectionSocket.send(endReply.encode())

    # send DATA TO Bob Mail Server
    SMTPClient(rcptServer, fromClient, msg)

    # send SUCCEED message
    global mailResponse
    if (mailResponse[:7] == 'Succeed'):
        succeedreply = 'Succeed!\r\n'
        connectionSocket.send(succeedreply.encode())

    # reply QUIT command
    data = connectionSocket.recv(1024).decode()
    if data[:4] == 'QUIT':
        print (data)
        quitReply = '221 Alice Mail Server closing connection\r\n'
        connectionSocket.send(quitReply.encode())
        connectionSocket.close()

    # send data to Bob Mail Server
def SMTPClient(rcptServer, fromClient, msg):
    print('SMTP Client\r\n')
    
    # Create socket called clientSocket and establish a TCP connection with receiver mail server
    mailserver = rcptServer.split(':')[0]
    mailport = eval(rcptServer.split(':')[1])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, mailport))

    # PROTOCOL
    protocol = 'SMTP\r\n'
    print('The protocl: '+protocol)
    clientSocket.send(protocol.encode())

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server. The service is not ready.')

    # Send HELO command and print server response.
    heloCommand = 'HELO ' + mailserver + '\r\n'
    print(heloCommand)
    clientSocket.send(heloCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server. The service is not ready.')

    # Send MAIL FROM command and print server response.
    MFCommand = 'MAIL FROM: <' + fromClient + '>\r\n'
    print(MFCommand)
    clientSocket.send(MFCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server. The service is not ready.')

    # Send RCPT TO command and print server response.
    RTCommand = 'RCPT TO: <' + rcptServer + '>\r\n'
    print(RTCommand)
    clientSocket.send(RTCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server. The service is not ready.')

    # Send DATA command and print server response.
    DATACommand = 'DATA\r\n'
    print(DATACommand)
    clientSocket.send(DATACommand.encode())
    recv = clientSocket.recv(1024)
    recv = recv.decode()
    print(recv)
    if recv[:3] != '354':
        print('354 reply not received from server. The service is not ready.')

    # Send message data.
    endmsg = "\r\n.\r\n"
    print(msg+endmsg)
    clientSocket.send((msg+endmsg).encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server. The service is not ready.')

    # Success message.
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:7] == 'Succeed':
        global mailResponse
        mailResponse = 'Succeed!\r\n'

    # Send QUIT command and get server response.
    QUITCommand = 'QUIT\r\n'
    print(QUITCommand)
    clientSocket.send(QUITCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '221':
        print('221 reply not received from server. The service is not ready.')

    clientSocket.close()

while True:
    # accecpt
    connectionSocket, addr = serverSocket.accept()
    print('Start SMTP server!\r\n')
    # SMTPServer function
    SMTPServer(connectionSocket)
