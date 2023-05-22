from scapy.all import *
import socketserver

from rudp_handler import MyRUDPHandler

load_layer('http')


class RedirectHandler(MyRUDPHandler):

    def handle(self):
        data = self.request[0].strip()

        self.send_ack_message()

        request = HTTP(
            data
        )

        print("{} wrote:".format(self.client_address[0]))
        print(request[HTTP])

        if request.Method == b'GET':
            if request.Path == b'/':
                message = HTTP() / HTTPResponse(
                    Status_Code=b'302',
                    Reason_Phrase=b'Found',
                    Location=b'http://localhost:30813/'
                )
            else:
                message = HTTP() / HTTPResponse(
                    Status_Code=b'404',
                    Reason_Phrase=b'Not Found'
                )

            self.retry_send_data_message(message.__bytes__())


if __name__ == "__main__":
    HOST, PORT = "localhost", 20021
    with socketserver.UDPServer((HOST, PORT), RedirectHandler) as server:
        server.serve_forever()
