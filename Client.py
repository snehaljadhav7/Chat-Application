from datetime import datetime
import tkinter as TK
from tkinter import Frame, Label, Text, END, Scrollbar, VERTICAL, Button
from tkinter import messagebox
import getpass
import threading
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import psycopg2
class Client:
    count = 1
    CLIENT = None
    last_received_message = None
    
    def __init__(self, argv, root):
        self.name = str(argv)
        self.root = root
        self.root.title("Chat Room") 
        self.root.resizable(0, 0)
        self.create_socket()
        self.display_name()
        self.chat_room()
        self.entry_box()
        self.listen_for_incoming_messages_in_a_thread()
	

    
    def create_socket(self):
        self.CLIENT = socket(AF_INET, SOCK_STREAM)
        host = '127.0.0.1'
        port = 10319
        self.CLIENT.connect((host, port))


    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.CLIENT,)) 
        thread.start()
  
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')      
            self.chat_room_area.insert('end', message + '\n')
            self.chat_room_area.yview(END)

        so.close()

 
   
    def chat_room(self):
        frame = Frame()	
        self.chat_room_area = Text(frame, width=60, height=10, font=("Calibri", 12))
        self.chat_room_area.bind('<KeyPress>', lambda e: 'break')
        scrollbar = TK.Scrollbar(frame, orient="vertical", command = self.chat_room_area.yview)
        self.chat_room_area.config(yscrollcommand=scrollbar.set)
        self.chat_room_area.pack(side='left', padx=10)
        frame.pack(side='top')
        scrollbar.pack(side='right', fill='y')

    def display_name(self):
        frame = Frame()
        user_name = 'User name: '+ self.name[2:-2]
        db_val = self.name[2:-2]
        conn = psycopg2.connect(user="postgres",
                                  password="pune1234",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres");
        dbCursor = conn.cursor();
        query = "INSERT INTO user_s (id, user_name, created_on)values(%s, %s, %s)";
        current_timestamp = datetime.now()
        data = (1, db_val,current_timestamp)
        dbCursor.execute(query, data);
        conn.commit()
        conn.close()
        Label(frame, text=user_name, font=("Calibri", 12, "bold")).pack(side='top', padx=10)
        frame.pack(side='top', anchor='n')
   
    def entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Calibri", 12)).pack(side='top', anchor='w')
        self.text_entry = Text(frame, width=60, height=3, font=("Arial", 12))
        self.text_entry.pack(side='left', pady=15)
        self.text_entry.bind('<Return>', self.data_entry)
        frame.pack(side='top')
        
    def data_entry(self, event):
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.text_entry.delete(1.0, 'end')

    def send_chat(self):
        frame = Frame()
        senders_name = str(self.name[2:-2]) + ": "
        data = self.text_entry.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
    
        frame.pack(side='top', anchor='nw')
        self.chat_room_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_room_area.yview(END)
        self.CLIENT.send(message)
        self.text_entry.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.CLIENT.close()
            exit(0)

if __name__ == '__main__':
    root = TK.Tk()
    cl = Client(sys.argv[1:],root)
    root.protocol("WM_DELETE_WINDOW", cl.on_close_window)
    root.mainloop()



