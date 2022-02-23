import threading
import socket

host = '127.0.0.1'
port = 50000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = []
nicknames = []


# The protocol between the users:
# To connect - just pick a user name.
# To get the list of the users that are online - just write 'get names'
# To send a message to the group - just write a message
# To send a private message to a user - just write at the beginning <nickname_destination> and then your message
# To disconnect - just write 'exit'



# a function to send a message for all the group
def brodcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode()
            index = clients.index(client)
            # if the client wants to disconnect
            if message == f'{nicknames[index]}: exit':
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                brodcast(f'{nickname} left the chat!'.encode())
                nicknames.remove(nickname)
                print(f'{nickname} left the chat!')
                break
            # if the client wants to get the names of the users that online
            elif message == f'{nicknames[index]}: get names':
                names_message = str(nicknames)
                clients[index].send(names_message.encode())
            # regular message or a private message
            else:
                count = 0
                flag = 1
                for nick in nicknames:
                    # checking if the message is a private message
                    if str("<"+str(nick)+">") in message:
                        private_msg = message.replace(str(nicknames[index]) + ": <" +str(nick)+">" , "PRIVATE - <" + str(nicknames[index])+"," + str(nick) + ">")
                        clients[count].send(private_msg.encode())
                        clients[index].send(private_msg.encode())
                        flag = 0
                        print("CHECK")
                    count += 1
                if flag:
                    brodcast(message.encode())
        # if an error occurred - automatically disconnect the client
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            brodcast(f'{nickname} left the chat!'.encode())
            nicknames.remove(nickname)
            print(f'{nickname} left the chat!')
            break


def recieve():
    while True:
        client, addr = server.accept()
        print(f"Connected with {str(addr)}")

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        brodcast(f'{nickname} joined the chat!'.encode())
        client.send('Connected to the server!'.encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server is listening...")
recieve()
