import socket
import sys
import easygui as eg
host= '192.168.1.126'
port=10000
def Search_Path():
    path_player= eg.diropenbox(msg="open",
                            title='Control',
                            default='.')
    return path_player
def main():

    id_user='-1'

    while True:

        print('Conectando al servidor')

        # WELCOME
        while True:
            try:
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mySocket.connect((host,port))

                msg_conn_true=mySocket.recv(1024).decode()
                print(msg_conn_true)

                msg_Estatus=mySocket.recv(1024).decode()
                print('hola32')
                if msg_Estatus == "Falso":
                    print('hola')
                    path_1=Search_Path()
                    msg_1=mySocket.recv(1024).decode()
                    print(msg_1)
                    mySocket.send(path_1.encode())
                mySocket.send(id_user.encode())

                msgWelcome=mySocket.recv(1024).decode()
                print(msgWelcome)

                break
            except:
                continue
        if id_user == '-1':
            while True:
                op_input=input('->')
                try:
                    mySocket.send(op_input.encode())

                except:
                    print('Servidor desconectado')
                try:
                    data=mySocket.recv(1024).decode()
                    print(data)
                    if op_input == "path":
                        print('new path')
                        path_1=Search_Path()
                        mySocket.send(path_1.encode())
                    if op_input == "salir":
                        print('chao')
                        mySocket.close()
                        return
                except:
                    print('servidor desconectado')
                    break

if __name__ == '__main__':
    main()