
import threading
import socket

# download file-billyjoel_music.txt
# download file-israeli_music.txt


host = '127.0.0.1'
port = 50000
byte_size = 500
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
clients = []
nicknames = []
file_names = []
available_port = [0 for i in range(0, 15)]
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# The protocol between the users:
# To connect - just pick a user name.
# To get the list of the users that are online - just write 'get names'
# To send a message to the group - just write a message
# To send a private message to a user - just write at the beginning <nickname_destination> and then your message
# To get the names of the files - just write 'get files'
# To download a file - just write "download file-'file name'"
# To disconnect - just write 'exit'


def read_file(file_name):
    f = open(file_name, "rb")
    data = f.read(500)
    list_data = [data]
    while data:
        data = f.read(500)
        list_data.append(data)
    f.close()
    return list_data


def download_udp(index, file_name):
    global port_listen
    flag = True
    for i in range(0, 15):
        if flag:
            if available_port[i] == 0:
                port_listen = i + 55002
                available_port[i] = 1
                for j in range(i + 1, 15):
                    if available_port[j] == 0:
                        port_ack = j + 55002
                        available_port[j] = 1
                        flag = False
                        socket_udp.bind((host, port_ack))
                        clients[index].send(f'starting udp download~ {port_listen, port_ack}'.encode())
                        break
    file_arr = read_file(file_name)
    for i in range(0, len(file_arr)):
        got_ack = True
        while got_ack:
            socket_udp.sendto(file_arr[i], ('127.0.0.1', port_listen))
            try:
                msg = socket_udp.recv(500).decode()
                if int(msg) == i:
                    got_ack = False
                    break
            except:
                continue
    clients[index].send(f'Download file done'.encode())
    socket_udp.sendto(f'mother'.encode(), ('127.0.0.1', port_listen))


# a function to send a message for all the group
def brodcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode()
            index = clients.index(client)
            split_msg = message.split('-')
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
            # if the client wants to get the names of the files in the server
            elif message == f'{nicknames[index]}: get files':
                files_message = str(file_names)
                clients[index].send(files_message.encode())
            # if the client wants to download a specific file
            elif split_msg[0] == f'{nicknames[index]}: download file':
                file_name = split_msg[1]
                if file_name in file_names:
                    udp_thread = threading.Thread(target=download_udp, args=(index, file_name))
                    udp_thread.start()
                else:
                    clients[index].send('there is no such a file'.encode())
            # regular message or a private message
            else:
                count = 0
                flag = 1
                for nick in nicknames:
                    # checking if the message is a private message
                    if str("<" + str(nick) + ">") in message:
                        private_msg = message.replace(str(nicknames[index]) + ": <" + str(nick) + ">",
                                                      "PRIVATE - <" + str(nicknames[index]) + "," + str(nick) + ">")
                        clients[count].send(private_msg.encode())
                        clients[index].send(private_msg.encode())
                        flag = 0
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


if __name__ == '__main__':
    print("server is listening...")
    file_names.append("billyjoel_music.txt")
    file_names.append("classic_music.txt")
    file_names.append("israeli_music.txt")
    recieve()