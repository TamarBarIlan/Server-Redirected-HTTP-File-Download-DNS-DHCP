from scapy.all import *
import socketserver

load_layer('http')


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        request = HTTP(
            self.request.recv(1024).strip()
        )

        print("{} wrote:".format(self.client_address[0]))
        print(request[HTTP])

        if request.Method == b'GET':
            if request.Path == b'/':
                response = HTTP() / HTTPResponse(
                    Status_Code=b'302',
                    Reason_Phrase=b'Found',
                    Location=b'http://localhost:8081/'
                )
            else:
                response = HTTP() / HTTPResponse(
                    Status_Code=b'404',
                    Reason_Phrase=b'Not Found'
                )

        self.request.sendall(response.__bytes__())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
