import socket
import threading

from config import *

LIST_OF_CLIENTS = {}


def handle_connection(connection: socket.socket, address: str) -> None:
    username = None
    try:
        username = register_user(connection, address)
        welcome_msg = bytes(f'Добро пожаловать {username} в чат-рум!',
                            CODING_TYPE)
        connection.send(welcome_msg)
        while True:
            data = connection.recv(MSG_LENGTH).decode(encoding=CODING_TYPE)
            if data == ':q':
                break
            broadcast(connection, data)
    except ConnectionError:
        pass
    finally:
        connection.close()
        if username is not None:
            remove(connection, username)


def register_user(connection: socket.socket, address: str) -> str:
    username = connection.recv(MSG_LENGTH).decode(encoding=CODING_TYPE)

    LIST_OF_CLIENTS[username] = {
        'address': address,
        'client': connection,
    }

    broadcast(connection, f'{username} присоеднился!')
    # logger.info(f'{address}:{nickname} joined the chat')

    return username


def broadcast(connection: socket.socket, msg: str) -> None:
    for username, client in LIST_OF_CLIENTS.items():
        if client['client'] != connection:
            try:
                client['client'].send(bytes(msg, CODING_TYPE))
            except:
                client['client'].close()
                remove(client, username)


def remove(connection: socket.socket, username: str) -> None:
    del LIST_OF_CLIENTS[username]
    broadcast(connection, f'{username} покинул чат.')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread_rcv = threading.Thread(target=handle_connection,
                                          args=[conn, addr],
                                          daemon=True)
            thread_rcv.start()
            # thread_rcv.join()
        # thread_snd.join()
    except KeyboardInterrupt:
        pass
    except (socket.error, ConnectionError):
        # logger.exception('Error occurred')
        pass
    finally:
        for user in LIST_OF_CLIENTS.values():
            user['client'].close()
        s.close()
