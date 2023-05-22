from scapy.all import *
import socketserver

load_layer('http')


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        request = HTTP(self.request.recv(1024).strip())

        if request.Method == b'GET':
            if request.Path == b'/':
                with open('home.html', 'rb') as f:
                    myfile = f.read()

                    response = HTTP() / HTTPResponse(
                        Content_Type=b'text/html;charset=utf-8',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile
            if request.Path == b'/cat.jpg':
                with open('cat.jpg', 'rb') as f:
                    myfile = f.read()

                    response = HTTP() / HTTPResponse(
                        Content_Type=b'image/jpeg',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile
            if request.Path == b'/cow.jpg':
                with open('cow.jpeg', 'rb') as f:
                    myfile = f.read()

                    response = HTTP() / HTTPResponse(
                        Content_Type=b'image/jpeg',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile
            if request.Path == b'/dog.jpg':
                with open('dog.jpg', 'rb') as f:
                    myfile = f.read()

                    response = HTTP() / HTTPResponse(
                        Content_Type=b'image/jpeg',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile

            self.request.sendall(response.__bytes__())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8081
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
