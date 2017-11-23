import socket
import vlc
import threading
from os import listdir
import os
import sys
host = '192.168.43.109'
port = 10000

class Media_player():
    def __init__(self):
        print('Ini object')
        self.path_player = None
        self.lista = []
        self.filename = None
        self.carpeta = None
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.isPaused = False
        self.Estado = False

    def GetEstado(self):
        return "True" if self.Estado else "Falso"

    def SetEstado(self, s):
        self.Estado=s
        return self.Estado

    def Search_Path(self):
        self.path_player = eg.diropenbox(msg="open",
                                         title='Control',
                                         default='.')
        return self.path_player

    def PlayPause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.isPaused = True
        else:
            self.mediaplayer.play()
            self.isPaused = False

    def Stop(self):
        self.mediaplayer.stop()

    def Next(self):
        self.Stop()
        if len(self.lista) is 0:
            return True
        self.Add_PlaybackVlc()

    def SetPath_player(self, new_path):
        self.lista=[]
        self.path_player = new_path
        return self.path_player

    def Crear_lista(self):
        if self.path_player is None:
            return
        self.carpeta = listdir(self.path_player)
        for filename in self.carpeta:
            k = len(filename)
            if filename[k - 3:k] != 'mp3':
                break
            dire = os.path.join(self.path_player, filename)
            print(dire)
            self.lista.append(dire)
        self.lista.reverse()
        return

    def GetFileName(self):
        return self.filename

    def Add_PlaybackVlc(self):
        if len(self.lista) == 0:
            return
        if self.mediaplayer.is_playing() :
            pass
        else:
            self.filename = self.lista.pop()
            self.media = self.instance.media_new(self.filename)
            self.mediaplayer.set_media(self.media)
            self.media.parse()
            play=threading.Thread(self.PlayPause(), args=None)
            play.start()
    def Update(self):
        pass

    def Volume(self, option):
        if option is 'max':
            self.mediaplayer.audio_set_volume(100)
        if option is 'min':
            self.mediaplayer.audio_set_volume(80)
        if option is 'mute':
            self.mediaplayer.audio_set_volume(0)
        return

def ClientThread(conn, addr, V):
    msg_conn_true = "F:\Bomba Estereo Elegancia tropical"
    conn.send(msg_conn_true.encode())
    msg_recivido=conn.recv(1024).decode()
    print(msg_recivido)
    msg_Estatus = V.GetEstado()
    conn.send(msg_Estatus.encode())
    print(msg_Estatus)
    if msg_Estatus == "Falso":
        print('search path')
        msg_1 = "Iniciando media player, porfavor indique el directorio de repodruccion\n"
        conn.send(msg_1.encode())
        while True:
            try:
                path_1 = conn.recv(1024).decode()
                break
            except:
                continue
        print(path_1)
        V.SetPath_player(path_1)
        V.Crear_lista()
        V.Add_PlaybackVlc()
        V.SetEstado(True)
        name = V.GetFileName()
        
    id_user = conn.recv(1024).decode()
    if id_user == '-1':
        msgWelcome = (" +------------------------+\n"
                      " |    MEDIAPLAYERLANNUS   |\n"
                      " | Elige una opcion:      |\n"
                      " | [play] :      PLAY     |\n"
                      " | [next] :      NEXT     |\n"
                      " | [stop] :      STOP     |\n"
                      " | [play] :      MUTE     |\n"
                      " | [next] :      VMAX     |\n"
                      " | [stop] :      VMIN     |\n"
                      " | [path] : NEW PATH FILES|\n"
                      " | [salir]: CLOSE CONEXION|\n"
                      " +------------------------+\n")
        conn.send(msgWelcome.encode())
        while True:
            try:
                log_op = conn.recv(1024).decode()
                print('en reproduccion:  ', name)
                if log_op == 'play':
                    print('play')
                    V.PlayPause()
                    conn.send(name.encode())
                elif log_op == 'next':
                    print('next')
                    V.Next()
                    name = V.GetFileName()
                    print('NEXT: ', name)
                    conn.send(name.encode())
                elif log_op == 'stop':
                    V.stop()
                    print('stop')
                    conn.send(name.encode())
                elif log_op == 'path':
                    V.stop()
                    print('new path')
                    path_1=None
                    path_1 = conn.recv(1024).decode()
                    print(path_1)
                    V.SetPath_player(path_1)
                    V.Crear_lista()
                    V.Add_PlaybackVlc()
                    print('path')
                elif log_op == 'mute':
                    print('mute')
                    V.Volume('mute')
                    conn.send('MUTE'.encode())
                elif log_op == 'max':
                    print('max')
                    V.Volume('max')
                    conn.send('VOLUMEN MAX'.encode())
                elif log_op == 'min':
                    print('min')
                    V.Volume('min')
                    conn.send('VOLUMEN MIN'.encode())
                elif log_op == 'salir':
                    conn.send("!Desconectado".encode())
                    print('close')
                    conn.close()
                    return
                else:
                    conn.send("+ Opcion invalida, intenta nuevamente\n".encode())
            except:
                conn.close()
                return
    conn.close()
    return

def main():
    V = Media_player()
    #Play_h=threading.Thread(target=V.Update()).start()
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind((host, port))
    mySocket.listen(2)
    print('Servidor funcionando')
    while True:
        try:
            conn, client_address = mySocket.accept()
            print('Cliente Nuevo', client_address)
            Cliente=threading.Thread(target=ClientThread,args=(conn,client_address,V))
            Cliente.daemon=True
            Cliente.start()
            Cliente.join()
            Cliente.exit()
            Cliente=None
        except:
            continue
    mySocket.close()


if __name__ == '__main__':
    main()
