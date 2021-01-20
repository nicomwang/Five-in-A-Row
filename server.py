import socket
from threading import Thread

host = ''
port = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)
print('Server started. Waiting for connection')

clients = []  # store connected ip in a list


def main():
    class ClientHandler(Thread):

        def __init__(self, client):
            super().__init__()
            self._client = client

        def run(self):
            while True:
                try:
                    data = self._client.recv(1024)
                    # remove the client who sent out data
                    clients.remove(self._client)
                    # send data to other client
                    for client in clients:
                        client.send(data)
                    # add removed client back
                    clients.append(self._client)
                except ConnectionResetError:
                    if self._client in clients:
                        # remove client if connection is lost
                        clients.remove(self._client)
                        print('Disconnected with a client')
                    else:
                        break

    while True:
        # current client
        curr_client, addr = server_socket.accept()
        clients.append(curr_client)
        print(addr[0], 'Connection established successfully！Connecting with %d client(s).' % len(clients))

        ClientHandler(curr_client).start()


if __name__ == '__main__':
    main()
