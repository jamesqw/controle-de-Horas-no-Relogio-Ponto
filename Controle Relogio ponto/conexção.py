import socket

class Servidor:
    def __init__(self, host='localhost', porta=5000):
        self.host = host
        self.porta = porta
        self.socket = socket.socket()
        
        # Inicia o servidor
        self.socket.bind((self.host, self.porta))
        self.socket.listen()
        
    def esperar_conexao(self):
        print('Aguardando conexão...')
        conn, addr = self.socket.accept()
        print(f'Conexão estabelecida com {addr}')
        return conn
    
    def enviar(self, conn, mensagem):
        conn.send(mensagem.encode())
        
    def receber(self, conn):
        mensagem = conn.recv(1024).decode()
        return mensagem
        
    def fechar(self):
        self.socket.close()

