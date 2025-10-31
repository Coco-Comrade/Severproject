import socket
import logging
import random
import os
from datetime import datetime
"""
Server Project-
Made: 2025
By: Omer Attia

This program opens a TCP server waits for a client and only allows up to 4 byte words to enter.
The server will have 4 outputs availble:
1. Current time
2.  random number
3. The name of the device the server is hosted on
4. A command that allows the client to disconnect from the server
All logs will be put in 'server.log'
"""
NOW = datetime.now()
SERVER_NAME = socket.gethostname()
QUEUE_LEN = 1
MAX_PACKET = 1024
LOG_PATH = os.path.join(os.path.dirname(__file__), 'serverpy.log')
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('0.0.0.0', 8820))
        server_socket.listen(QUEUE_LEN)
        logging.info('Listening on port 8820')
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info('Accepted connection from {}'.format(client_address))
            try:
                while True:
                    handled = True
                    response = "Error unkown command given"
                    request = client_socket.recv(MAX_PACKET).decode().strip()
                    assert len(request) <= 4, f"Command too long: {len(request)}"
                    logging.info('Received {}'.format(request))
                    if request == 'TIME':
                        response = datetime.now().strftime("%H:%M:%S")
                        logging.info('Sent local time')
                    elif request == 'EXIT':
                        client_socket.close()
                        logging.info('Server exited')
                    elif request == 'NAME':
                        response = ("Server name :"+SERVER_NAME)
                        logging.info('Sent server name')
                    elif request == 'RAND':
                        response = f'Random number: {random.randint(1, 10)}'
                        logging.info('Sent random number generator')
                    elif request == "QUEUE":
                        response = "Queue :" + str(QUEUE_LEN)
                        logging.info('Sent queue length')
                    else:
                        handled = False
                    if not handled:
                        logging.error('Received unknown command')
                    client_socket.send(response.encode())
            except socket.error as err:
                logging.error('Socket error {}'.format(err))

    except socket.error as err:
        logging.error('Socket error {}'.format(err))
    finally:
        server_socket.close()
        logging.info('Closing server')
if __name__ == "__main__":
    main()