import socket
import threading


def send_message():
    i = 0
    print(f"Connected to server..! ")
    print(f"To exit chat room type exit..! ")
    while True:
        try:
            if i == 0:
                message = input('Enter Your username : ')
                message = message.encode('utf-8')
                message_size = f"{len(message):<{def_len}}".encode('utf-8')
                client_socket.send(message_size + message)
            else:
                message = input('Enter your message : ')
                if message == "exit":
                    client_socket.close()
                else:
                    message = message.encode('utf-8')
                    message_size = f"{len(message):<{def_len}}".encode('utf-8')
                    client_socket.send(message_size + message)
        except:
            pass
        i = i + 1

def recv_message(cli_socket):
        try:
            while True:
                cli_msg_len = cli_socket.recv(def_len)
                if cli_msg_len:
                    cli_msg_len = int(cli_msg_len.decode('utf-8').strip())
                    #print(f"{cli_socket.recv(cli_msg_len)}".decode('utf-8'))
                    client_message = cli_socket.recv(cli_msg_len)
                    client_message = client_message.decode('utf-8')
                    print(client_message)
            else:
                print(f"error recieving message")
        except:
            pass


if __name__ == "__main__":
    def_len = 10
    HOST = 'localhost'
    PORT = 2345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))


    send_thread = threading.Thread(target = send_message)
    send_thread.start()
    recv_thread = threading.Thread(target = recv_message, args = [client_socket])
    recv_thread.start()
