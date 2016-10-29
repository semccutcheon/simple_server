from socket import *
import threading
import sys # In order to terminate the program

class server():
    def __init__(self, port):
        self.port = port
        self.ip = ''
        self.threads = []

    def start_socket(self):
        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.bind((self.ip, self.port))
            self.server.listen(10)
        except OSError as err:
            if self.server:
                self.server.close()
            print(err)
            sys.exit(1)
        
    
    def run(self):
        self.start_socket()
        run = True
        while run:
            try:
                c = Client(self.server.accept())
                c.start()   
                self.threads.append(c)
            except KeyboardInterrupt:
                run = False
        for thrd in self.threads:
            thrd.join()


class Client(threading.Thread):
    def __init__(self, conn):
         threading.Thread.__init__(self)
         self.clientSocket = conn[0]
         self.address = conn[1]
         self.size = 1024

    def run(self):
        message = self.clientSocket.recv(self.size).decode()
        filename = message.split()[1][1:]
        try:
            with open(filename) as f:
                data = f.read()
            
            okay = "HTTP/1.1 200 OK\n Content-Type: text/html\n\n".encode()
            self.clientSocket.send(okay)
            for i in range(0, len(data)):
                self.clientSocket.send(data[i].encode())

            self.clientSocket.send("\r\n".encode())
            self.clientSocket.close()

        except FileNotFoundError:
            not_found = "HTTP/1.1 404 Not Found\n \n\n".encode()
            self.clientSocket.send(not_found)
            self.clientSocket.close()

s = server(8888)
s.run()

      