import socket
import threading

nickname = input("Choose the nickname:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 50000))


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("Error")
            client.close()
            break


def write():
    while True:
        msg = input("")
        message = f'{nickname}: {msg}'
        client.send(message.encode())


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
