# Originally coded by Yashraj Singh Chouhan 
# link: https://hackernoon.com/creating-command-line-based-chat-room-using-python-oxu3u33
import pandas as pd
import socket, threading

class ServerSide:
    def __init__(self, host = '127.0.0.1', port = 7976):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []

    def broadcast(self, message):  
        for client in self.clients:
            client.send(message)

    def handle(self, client):                                         
        while True:
            try: 
                message = client.recv(1024)
                self.broadcast(message)
            except: 
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('ascii'))
                self.nicknames.remove(nickname)
                break

    def receive(self, server): 
        while True:
            client, address = server.accept()
            print("Connected with {}".format(str(address)))       
            client.send('NICKNAME'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.nicknames.append(nickname)
            self.clients.append(client)
            print("Nickname is {}".format(nickname))
            self.broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def deploy_chat_room(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        self.receive(server)

if __name__=="__main__":
    hosts_ports = pd.read_csv('hosts_port.csv').values
    for item in hosts_ports:
        print(f'Running server on host={item[0]}, port={item[1]}')
        mainThread = threading.Thread(target=ServerSide(host=item[0], port=item[1]).deploy)
        mainThread.start()