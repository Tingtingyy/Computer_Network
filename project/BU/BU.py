# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 09:42:30 2021

@author: hp
"""


from flask import Flask,Response,request
#from werkzeug.exceptions import HTTPException
from socket import *
BU = Flask(__name__)
BU.config['ENV'] = 'development'


@BU.route('/email')
def getemail():
    address=request.args.get('from')
    #print('The server address passed in:'+address)
    al=address.split(':')
    serverName = al[0]
    print(serverName)
    serverPort = eval(al[1])
    print(serverPort)
    POP3client(serverName, serverPort)
    return str(MailBox)
    

@BU.errorhandler(Exception)
def handle_exception(e):
    return Response('Bad request!',400)

def POP3client(serverName,serverPort):
    BUSocket=socket(AF_INET,SOCK_STREAM)
    BUSocket.connect((serverName,serverPort))
    username = 'Bob'
    password = '112'
    END = '\r\n.\r\n'
    
    # protocol choice
    Protocolchoice ='POP3\r\n'
    print('protocol: '+Protocolchoice)
    BUSocket.send(Protocolchoice.encode())
    response = BUSocket.recv(1024).decode()
    print(response)
    if response[:3] != '+OK':
        print('correct reply was not received!')
    
    # Send user and password command
    user = 'user: '+username+'\r\n'
    print(user)
    BUSocket.send(user.encode())
    response1 = BUSocket.recv(1024).decode()
    print(response1)
    if response1[:3] != '+OK':
        print('correct reply was not received!')
    passcommand = 'pass: '+password+'\r\n'
    print(passcommand)
    BUSocket.send(passcommand.encode())
    response2 = BUSocket.recv(1024).decode()
    print(response2)
    if response2[:3] !='+OK':
        print('correct reply was not received!')
    
    # Send list command
    listcommand = 'list\r\n'
    print(listcommand)
    BUSocket.send(listcommand.encode())
    listinfo = []
    while True:
        listresponse = BUSocket.recv(1024).decode()
        if END in listresponse:
            listinfo.append(listresponse[:listresponse.find(END)])
            break
        listinfo.append(listresponse)
        if(len(listresponse)>1):
            lasttwolist = listinfo[-1]+listinfo[-2]
            if END in lasttwolist:
                listinfo[-2] = lasttwolist[:lasttwolist.find(END)]
                listinfo.pop()
                break
    liststring = ''.join(listinfo)+END
    print(liststring)
    
    # create an empty MailBox
    global MailBox
    MailBox = []
    
    # if there is no email return empty MailBox
    if(liststring==END):
        return
    
    # Count the number of emails(minus END Symbol)
    mailnumber = len(liststring.splitlines())-1
    
    
    # get every mail content in MailBox
    for index in range(mailnumber):   
        #RETR
        retrcommand='retr '+str(index+1)+'\r\n'
        print(retrcommand)
        BUSocket.send(retrcommand.encode())
        contentID = []
        while True:
          content = BUSocket.recv(1024).decode()
          if END in content:
              contentID.append(content[:content.find(END)])
              break
          contentID.append(content)
          if(len(contentID)>1):
              Lasttwo = contentID[-2]+contentID[-1]
              if END in Lasttwo:
                  contentID[-2] = Lasttwo[:Lasttwo.find(END)]
                  contentID.pop()
                  break
        mailcontentID=''.join(contentID)
        print(mailcontentID+END)
        # store every mail content into the MailBox
        MailBox.append(mailcontentID)        
        #DELE
        delecommand = 'dele'+str(index+1)+'\r\n'
        print(delecommand)
        BUSocket.send(delecommand.encode())
    
    # send quit command
    logoff='quit\r\n'
    print(logoff)
    BUSocket.send(logoff.encode())
    logoffresponse= BUSocket.recv(1024).decode()
    print(logoffresponse)
    if logoffresponse[:3] != '+OK':
        print('correct reply was not received!')
    BUSocket.close()
    
    # return the MailBox
    return MailBox
          

BU.run(host='0.0.0.0',
        port=6060,
        debug=True)

