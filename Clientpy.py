import socket

MAX_PACKET = 1024
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    my_socket.connect(('127.0.0.1', 8820))

    while True:
        print("Please insert the following commands: TIME, RAND, NAME, EXIT")
        X = input()
        my_socket.send(X.encode())
        response = my_socket.recv(MAX_PACKET).decode()
        if X == "EXIT":
            my_socket.close()
            break
        print(response)
except socket.error as err:
    print('received socket error ' + str(err))
finally:
    my_socket.close()