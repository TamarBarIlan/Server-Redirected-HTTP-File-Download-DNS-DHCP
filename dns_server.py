from scapy.all import *
import socketserver

DNS_RECORDS = {
    b'first.domain.': b'1.2.3.4',
    b'second.domain.': b'5.6.7.8'
}


class DNSProtocolHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        dns_layer = DNS(data)
        qname = dns_layer[DNSQR].qname

        if qname in DNS_RECORDS:
            # indicates that domain name found
            dns_layer[DNS].an = DNSRR(rrname=qname, rdata=DNS_RECORDS[qname])
            dns_layer[DNS].ancount = 1
        else:
            # indicates that domain name not found
            dns_layer[DNS].rcode = 'name-error'
            dns_layer[DNS].an = DNSRRSOA()

        sock.sendto(dns_layer.__bytes__(), self.client_address)


if __name__ == "__main__":
    HOST, PORT = "localhost", 53
    with socketserver.UDPServer((HOST, PORT), DNSProtocolHandler) as server:
        server.serve_forever()
