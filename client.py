import socket
import threading

from config import *


def receive(connection: socket.socket) -> None:
    while True:
        try:
            data = connection.recv(MSG_LENGTH).decode(encoding=CODING_TYPE)
            if not data:
                print('Чат больше не работает')
                break
            print(data)
        except:
            continue
        finally:
            connection.close()


def send(connection: socket.socket) -> None:
    try:
        username = bytes(input('Напиши свой никнейм:'), CODING_TYPE)
        connection.send(username)
        print('Чтобы выйти из чата, напишите кобминацию ":q" и отправьте.')
        while True:
            # data = bytes(input(), CODING_TYPE)
            data = input('')
            connection.send(data.encode(encoding=CODING_TYPE))
            if data == ':q':
                connection.send(data)
                break
    except ConnectionError:
        print('### Connection lost ###')



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        thread_rcv = threading.Thread(target=receive,
                                      args=[s],
                                      daemon=True)
        thread_snd = threading.Thread(target=send,
                                      args=[s],
                                      daemon=True)
        thread_snd.start()
        thread_rcv.start()
        thread_rcv.join()
        thread_snd.join()
    except ConnectionRefusedError:
        print('### Connection refused ###')
    except KeyboardInterrupt:
        pass
    finally:
        print('### You have been disconnected ###')
        if s is not None:
            s.close()
