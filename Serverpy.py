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
All logs will be put in 'serverpys.log'
"""
SERVER_NAME = socket.gethostname()
IP = "0.0.0.0"
PORT = 8820
QUEUE_LEN = 1
MAX_PACKET = 1024
LOG_PATH = os.path.join(os.path.dirname(__file__), 'serverpys.log')
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)



def handle_command(command: str) -> str:
    """Processes the 4 byte command and returns the appropriate response"""
    assert isinstance(command, str),"Command must be a string"
    assert len(command) <= 4, "Command must be equal or less then 4 letters"
    if command == 'TIME':
        logging.info('Sent local time')
        return datetime.now().strftime("%H:%M:%S")
    elif command == 'EXIT':
        logging.info('Client requested to exit the server')
        return "Bye!"
    elif command == 'NAME':
        logging.info('Sent server name')
        return SERVER_NAME
    elif command == 'RAND':
        num = random.randint(1, 10)
        logging.info('Sent random number between 1 and 10')
        return str(num)
    else:
        logging.error('Unknown command received: {command}')
        return "Unknown command"



def main():
    logging.info('Server started')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(QUEUE_LEN)

    logging.info(f'Server listening on port: {PORT}')
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info('Client connected')

            try:
                while True:
                    try:
                        data = client_socket.recv(MAX_PACKET).decode().strip()
                    except socket.error as err:
                        logging.error(f"Socket error: {err}")
                        break
                    if not data:
                        logging.info('Client disconnected')
                    logging.info(f"Data received: {data}")
                    try:
                        response = handle_command(data)
                        client_socket.send(response.encode())
                    except AssertionError as e:
                        response = str(e)
                        logging.error(f"Exception raised: {e}")

                    if data == 'EXIT':
                        logging.info('Client disconnected')
                        client_socket.close()
            finally:
                client_socket.close()
    finally:
        server_socket.close()
        logging.info('Server closed')
if __name__ == "__main__":
    main()