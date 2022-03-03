import socket
import threading

host = '127.0.0.1'
nickname = input("Choose the nickname:")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, 50000))
not_finish = True


def receive_file(port_listen, port_hack):
    print("GOT INSIDE THE THREAD RECIEVE FILE")
    client_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket_udp.bind((host, port_listen))
    print(port_listen , port_hack)
    recv_packets = []
    # index_packet = []
    # num_of_packets = client_socket_udp.recv(1024).decode()
    # client_socket_udp.send(b'cool, thanks')

    # while not_finish:
    #
    #     tmp_msg = client_socket_udp.recv(1024).decode()
    #     packet_num = int.from_bytes(tmp_msg[0:3], byteorder='big')
    #     if packet_num not in index_packet:
    #         client_socket_udp.settimeout()
    #         recv_packets.append(tmp_msg[3:len(tmp_msg)])
    #     client_socket_udp.sendto(str(packet_num).encode(), (host, port_sender))
    # not_finish = True

    while not_finish:
        tmp_msg = client_socket_udp.recv(1024).decode()
        recv_packets.append(tmp_msg)
        print(recv_packets)
        client_socket_udp.sendto(str(len(recv_packets) - 1).encode(), (host, port_hack))
    print("poopopopopop")
    client_socket_udp.close()
    f = open("recv_packets.txt", "w")
    for i in recv_packets:
        print("LDLDLDLD")
        f.write(i)
    f.close()

    # print("poopopopopop")
    # client_socket_udp.close()
    # f = open("recv_packets.txt", "w")
    # for i in recv_packets:
    #     print("LDLDLDLD")
    #     f.write(i)
    # f.close()



    # file open ...
    # add the recv packets in to the file


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
                print(listener_sender)
                print(listener_sender[0][2:7])
                print(listener_sender[1][1:6])
                port_listen = int(listener_sender[0][2:7])  # add substring
                port_sender = int(listener_sender[1][1:6])
                print(port_listen , port_sender)
                recive_file_thread = threading.Thread(target=receive_file, args=[port_listen, port_sender])
                recive_file_thread.start()
            elif message == 'Download file done':
                print("WE FINISHED WITH THIS SHIT")
                not_finish = False

            else:
                print(message)
        except:
            print("Error - MadaFucka")
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
