from scapy.all import *
import socketserver

from rudp_handler import MyRUDPHandler

load_layer('http')


class DownloadHandler(MyRUDPHandler):

    def handle(self):
        data = self.request[0].strip()

        self.send_ack_message()

        request = HTTP(
            data
        )

        if request.Method == b'GET':
            if request.Path == b'/':
                with open('home.html', 'rb') as f:
                    myfile = f.read()

                    message = HTTP() / HTTPResponse(
                        Content_Type=b'text/html;charset=utf-8',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile
            if request.Path == b'/cat.jpg':
                with open('cat.jpg', 'rb') as f:
                    myfile = f.read()

                    message = HTTP() / HTTPResponse(
                        Content_Type=b'image/jpeg',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile
            if request.Path == b'/cow.jpg':
                with open('cow.jpeg', 'rb') as f:
                    myfile = f.read()

                    message = HTTP() / HTTPResponse(
                        Content_Type=b'image/jpeg',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile
            if request.Path == b'/dog.jpg':
                with open('dog.jpg', 'rb') as f:
                    myfile = f.read()

                    message = HTTP() / HTTPResponse(
                        Content_Type=b'image/jpeg',
                        Content_Length=bytes(str(len(myfile)), encoding='utf-8')
                    ) / myfile

            self.retry_send_data_message(message.__bytes__())


if __name__ == "__main__":
    HOST, PORT = "localhost", 30813
    with socketserver.UDPServer((HOST, PORT), DownloadHandler) as server:
        server.serve_forever()

