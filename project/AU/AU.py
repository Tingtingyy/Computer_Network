from flask import Flask, Response, request
from socket import *

AU = Flask(__name__)
AU.config['ENV'] = 'development'

@AU.route('/email')
def email():
    fromaddress = request.args.get('from')
    message = request.args.get('message')
    toaddress = request.args.get('to')
    mailserver = fromaddress.split(':')[0]
    mailport = eval(fromaddress.split(':')[1])
    msg = message 
    SMTPClient(mailserver, mailport, fromaddress, toaddress, msg)
    return mailResponse


@AU.errorhandler(Exception)
def handle_exception(e):
    return Response('Bad request!', 400)


def SMTPClient(mailserver, mailport, fromaddress, toaddress, msg):
    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, mailport))

    global mailResponse
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
        print('250 reply not received from server. There may have some mistakes.')

    # Send MAIL FROM command and print server response.
    MFCommand = 'MAIL FROM: <' + fromaddress + '>\r\n'
    print(MFCommand)
    clientSocket.send(MFCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server. There may have some mistakes.')

    # Send RCPT TO command and print server response.
    RTCommand = 'RCPT TO: <' + toaddress + '>\r\n'
    print(RTCommand)
    clientSocket.send(RTCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server. There may have some mistakes.')

    # Send DATA command and print server response.
    DATACommand = 'DATA\r\n'
    print(DATACommand)
    clientSocket.send(DATACommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '354':
        print('354 reply not received from server. There may have some mistakes.')

    # Send message data.
    endmsg = "\r\n.\r\n"
    print(msg+endmsg)
    clientSocket.send((msg+endmsg).encode())
    # Message ends with a single period.   
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server. There may have some mistakes.')

    # Success message.
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:7] == 'Succeed':
        mailResponse = 'Succeed!\r\n'

    # Send QUIT command and get server response.
    QUITCommand = 'QUIT\r\n'
    print(QUITCommand)
    clientSocket.send(QUITCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '221':
        print('221 reply not received from server. There may be some mistake.')

    clientSocket.close()


AU.run(host='0.0.0.0',
        port=5000,
        debug=True)