from scapy.all import *
import socket


server_address = ('localhost', 53)

dns_req = DNS(rd=1, qd=DNSQR(qname='first.domain'))


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(dns_req.__bytes__(), server_address)
resp = DNS(s.recv(1024))
print(resp[DNSRR].rrname)
