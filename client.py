import socket
import threading

host = '127.0.0.1'
nickname = input("Choose the nickname:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 50000))
not_finish = True
recv_packets = []
flags = True


def receive_file(port_listen, port_hack):
    print("GOT INSIDE THE THREAD RECEIVE FILE")
    recv_packets.clear()
    client_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket_udp.bind((host, port_listen))
    # recv_packets = []
    while not_finish:
        tmp_msg = client_socket_udp.recv(500).decode()
        recv_packets.append(tmp_msg)
        client_socket_udp.sendto(str(len(recv_packets) - 1).encode(), (host, port_hack))


    print("I GOT OUT OF THE WHILE LOOP")
    client_socket_udp.close()
    f = open("recv_packets.txt", "w")
    for i in recv_packets:
        f.write(i)
    f.close()


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            split_msg = message.split('~')
            if message == 'NICK':
                client.send(nickname.encode())
            elif split_msg[0] == 'starting udp download':
                print("GOT INTO DOWNLOAD")
                listener_sender = split_msg[1].split(',')
                port_listen = int(listener_sender[0][2:7])
                port_sender = int(listener_sender[1][1:6])
                recive_file_thread = threading.Thread(target=receive_file, args=[port_listen, port_sender])
                recive_file_thread.start()
            elif message == 'Download file done':
                print("WE FINISHED WITH THIS SHIT")
                not_finish = False
                # client_socket_udp.close()
                f = open("recv_packets.txt", "w")
                for i in recv_packets:
                    f.write(i)
                f.close()
                print("DONE WITH THIS - LOOK UP")
            else:
                print(message)
        except:
            print("Error")
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
