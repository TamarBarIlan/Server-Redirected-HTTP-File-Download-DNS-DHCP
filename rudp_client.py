import socket
from urllib.parse import urlparse

def send_request(hostname, port, path):
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # connect to the server
    client_socket.connect((hostname, port))

    # create the GET request
    request = "GET " + path + " HTTP/1.1\r\nHost: " + hostname + "\r\n\r\n"

    # send the request to the server
    client_socket.send(request.encode())

    # receive ack from the server
    response = client_socket.recv(1024).decode()
    print("Response from server: ", response)

    # receive the data from the server
    data = client_socket.recv(1024).decode()
    print("Data from server: ", data)

    # send an ACK to the server
    client_socket.send("ACK".encode())

    # close the connection
    client_socket.close()

    # return the data
    return data

# example usage
data = send_request('localhost', 20021, "/")
print(data)

# check if the response has a status code of 302
if "302 Found" in data:
    # extract the new location from the response
    new_url = data.split("Location: ")[1].split("\r\n")[0]
    print("new location", new_url)

    parsed_url = urlparse(new_url)
    new_hostname = parsed_url.hostname
    print("new_hostname = ", new_hostname)
    new_port = parsed_url.port
    print("new_port = ", new_port)
    new_path = parsed_url.path
    print("new_path = ", new_path)

    # make a new connection to the new location
    new_data = send_request(new_hostname, new_port, new_path)
    # print("new data = ", new_data)