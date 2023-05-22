import socketserver


class MyRUDPHandler(socketserver.BaseRequestHandler):
    def send_ack_message(self):
        # send ACK message to client address
        self.request[1].sendto(b'ACK', self.client_address)

    def send_data_message(self, data, wait_for_ack=True):
        # send scapy message to client address
        self.request[1].sendto(data, self.client_address)

        if wait_for_ack:
            self.request[1].settimeout(5)
            try:
                data = self.request[1].recv(1024).strip()
                return data == b'ACK'
            except TimeoutError:
                return False
        else:
            return True

    def retry_send_data_message(self, data, count=3):
        ack = False
        while not ack and count:
            ack = self.send_data_message(data)
            if not ack:
                # no ACK received need to subtract 1 from count
                count -= 1
            else:
                break

        # check if no ACK received after while loop is over
        if not ack:
            raise Exception('no ACK from {}'.format(self.client_address))
