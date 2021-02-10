from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR



def accept_connections():
   while True:
      
      client= SERVER.accept()
      client_addr, (ip, port)= client
   
      
   
      if client not in Clients:
         Clients.append(client)
      print('Connected to ', ip, ':', port)
 
      th = Thread(target=receive_messages, args=(client_addr,))
      th.start()

def receive_messages(client_addr):
   while True:
      messages_received = client_addr.recv(256)
      if not messages_received:
         break
      last_received_message = messages_received.decode('utf-8')
      for client in Clients:
         socket,(ip, port) = client
         if socket is not client_addr:
            socket.sendall(last_received_message.encode('utf-8'))
 
   client_addr.close()
  
Clients = []



SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
HOST = '127.0.0.1'
PORT = 10319
addr = (HOST, PORT)
SERVER.bind(addr)

print("Waiting for connection ....")

SERVER.listen(5)
accept_connections()      






 





