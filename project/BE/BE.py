# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 11:04:52 2021

@author: hp
"""


from socket import *
serverPort = 53533
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
endmsg = '\r\n.\r\n'

# SMTP server
def SMTPserver(connectionSocket):
    # reply 220 smtp server ready
    reply = "220 Bob mail server\r\n"
    connectionSocket.send(reply.encode())
       
    # reply HELO command
    command1 = connectionSocket.recv(1024).decode()
    print(command1)
    if(command1[:4]=='HELO'):
        reply1 = '250 Hello,pleased to meet you\r\n'
        connectionSocket.send(reply1.encode())
   
    # reply MAIL FROM command
    command2 = connectionSocket.recv(1024).decode()
    print(command2)
    if(command2[:9] =='MAIL FROM'):
        reply2 = '250 Alice Sender oK\r\n'
        connectionSocket.send(reply2.encode())
   
    # reply RCPT TO command
    command3 = connectionSocket.recv(1024).decode()
    print(command3)
    if(command3[:7] == 'RCPT TO'):
        reply3 = '250 Bob Mail Server Recipent oK\r\n'
        connectionSocket.send(reply3.encode())
    
    # reply DATA command
    command4 = connectionSocket.recv(1024).decode()
    print(command4)
    if(command4[:4] == 'DATA'):
        reply4 = '354 Enter mail, end with "." on a line by itself\r\n'
        connectionSocket.send(reply4.encode())
    
    # receive mail data with end symbol
    Mailcontent = []
    while True:
      Realdata = connectionSocket.recv(1024).decode()
      if endmsg in Realdata:
          Mailcontent.append(Realdata[:Realdata.find(endmsg)])
          break
      Mailcontent.append(Realdata)
      # check if end symbol is split
      if len(Mailcontent)>1:
          Lasttwo = Mailcontent[-2] + Mailcontent[-1]
          if endmsg in Lasttwo:
              Mailcontent[-2] = Lasttwo[:Lasttwo.find(endmsg)]
              Mailcontent.pop()
              break
    Everymailcontent = ''.join(Mailcontent)
    print(Everymailcontent+endmsg)
    reply5 = '250 Message accepted for delivery\r\n'
    connectionSocket.send(reply5.encode())
    
    # save the content of each mail into a local file
    f = open('Totallocalmail.txt','a')
    f.write(Everymailcontent+'\n.\n')
        
    #Send Success command
    succeedreply='Succeed!\r\n'
    connectionSocket.send(succeedreply.encode())
    
    # reply QUIT command     
    quitcommand = connectionSocket.recv(1024).decode()
    print(quitcommand)
    if(quitcommand[:4]=='QUIT'):
        reply6 ='221 Bob mail server closing connection\r\n'
        connectionSocket.send(reply6.encode())
        connectionSocket.close()
    
# POP3server
def POP3server(connetionSocket):
    print('Start POP3 server!\r\n')
    replyOK = '+OK\r\n'
    replyError = '-ERR\r\n'
    reply = '+OK POP3 server ready\r\n'
    connectionSocket.send(reply.encode())

    # reply log in command
    command1 = connectionSocket.recv(1024).decode()
    print(command1)    
    if command1[:4]=='user':
        connectionSocket.send(replyOK.encode())
    else:
        connectionSocket.send(('-ERR user command was not correctly received\r\n').encode())
    command2 = connectionSocket.recv(1024).decode()
    print(command2)
    if command2[:4]=='pass':
        connectionSocket.send(('+OK user successfully logged on!\r\n').encode())
    else:
        connectionSocket.send(replyError.encode())
    
    # reply list command
    command3 = connectionSocket.recv(1024).decode()
    print(command3)
    replyList = ''
    try:
        with open('Totallocalmail.txt','r') as f:
            maildata=f.read()
        mailContent=maildata.split('\n.\n')
        mailContent.pop() 
    except IOError:
        # prevent there is no email received
        mailContent = []
        print('There is no email!')
    
    if command3[:4]=='list':
        for i in range(len(mailContent)):
            if(i<len(mailContent)-1):
              replyList += str(i+1)+" "+str(len(mailContent[i]))+'\r\n'
            else:
              replyList += str(i+1)+" "+str(len(mailContent[i]))
        replyList += '\r\n.\r\n'
        connectionSocket.send(replyList.encode())
    
    
   # reply retr command
    for index in range(len(mailContent)):
        command4 = connectionSocket.recv(1024).decode()
        print(command4) 
        if command4[:4]=='retr':
            ID = int(command4[5])
            print('getting the content of '+str(ID)+'th mail\r\n')
            if index!=ID-1:
                print('command ID and reply ID is not consistent!\r\n')
            print(mailContent[index]+endmsg)
            connectionSocket.send((mailContent[index]+endmsg).encode())
        #DELE REPLY
        command5 = connectionSocket.recv(1024).decode()
        print(command5)
        if command5[:4]=='dele':
            print('deleting the retrieved mail\r\n')
          
        
    # reply quit command
    logoffcommand = connectionSocket.recv(1024).decode()
    print(logoffcommand)
    if(logoffcommand[:4]=='quit'):
        logoffreply= '+OK pop3 server signing off\r\n'
        connectionSocket.send(logoffreply.encode())    
    else:
        connectionSocket.send(replyError.encode())
    connectionSocket.close()
     
    
    
while True:
    connectionSocket,addr = serverSocket.accept()
    Protocol = connectionSocket.recv(1024).decode()
    if(Protocol=='SMTP\r\n'):
        SMTPserver(connectionSocket)  
    if(Protocol=='POP3\r\n'):
        POP3server(connectionSocket)

    
    
    



