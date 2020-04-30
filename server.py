import socket
import select
import threading

def accept_client(client_socket, client_address):
    client_message = []
    while True:
        message = recv_message(client_socket)
        if message:
            client_message.append(message)
            i = client_message.index(message)
            if i == 0:
                print(f"{client_address[0]} set their username as :  {message}")
                broadcast_msg = f"{client_address[0]} set their username as :  {message}"
                broadcast(client_socket, broadcast_msg)
            else:
                print(client_message[0], ' says : ', client_message[i])
                broadcast_msg = f"{client_message[0]} says : {client_message[i]}"
                broadcast(client_socket, broadcast_msg)
        else:
            i = socket_list.index(client_socket)
            socket_list.remove(client_socket)
            client_list.remove(client_list[i-1])
            broadcast_msg = f"No. of people online = {len(client_list)}"
            broadcast(client_socket, broadcast_msg)

def recv_message(cli_socket):
    try:
        cli_msg_len = cli_socket.recv(def_len)
        if cli_msg_len:
            cli_msg_len = int(cli_msg_len.decode('utf-8').strip())
            return{cli_socket.recv(cli_msg_len).decode('utf-8')}
        else:
            return False
    except:
        pass

def broadcast(socket, message):
    for sock in socket_list:
        if sock != server_socket and sock != socket:
            try:
                message = message.encode('utf-8')
                message_size = f"{len(message):<{def_len}}".encode('utf-8')
                sock.send(message_size + message)
            except:
                socket.close()
                if socket in socket_list:
                    socket_list.remove(socket)
                    print(f"No. of people online : {len(socket_list)}")


client_list = []

if __name__ == "__main__":
    def_len = 10
    HOST = 'localhost'
    PORT = 2345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    socket_list = [server_socket]
    print("Listening for connections")
    while True:
        client_socket, client_address = server_socket.accept()
        client_list.append(client_address)
        socket_list.append(client_socket)
        print(client_address[0], ' : ', client_address[1], 'has connected to the chat room')
        client_thread = threading.Thread(target = accept_client, args = [client_socket, client_address])
        client_thread.start()
