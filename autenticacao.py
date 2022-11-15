import socket
import pickle
import threading
import time

PORT = 5050
FORMATO = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def login():
    print('\n--- Faça o Login para poder votar ---\n')
    login = str(input('Login: '))
    senha = str(input('Senha: '))

    credenciais = [login, senha]
    credenciais_serializada = pickle.dumps(credenciais)
    
    if autenticar(credenciais_serializada) == 'sucesso':
        return True
    else:
        return False

def autenticar(credenciais_serializada):
    client.send(credenciais_serializada)
    resposta = client.recv(4096).decode()
    return resposta

while True:
    if login():
        print('\n\n\n+-----CANDIDATOS DISPONÍVEIS-----+\n\nEm quem você vai votar?\n')
        data = client.recv(4096)
        candidatos = pickle.loads(data)

        def listar():
            for candidato in candidatos:
                print(f"{candidato['numero']} - {candidato['nome']}")
                
        while True:
            listar()
            candidato_escolhido = int(input('\nVote pelo número: '))
            existe = False
            for candidato in candidatos:
                if candidato_escolhido in candidato.values():
                    existe = True
                    voto = candidato['nome'], candidato['numero']
                    break
            
            if existe:
                break
        client.send(pickle.dumps(voto))
        print('VOTO CONFIRMADO COM SUCESSO!')
        break

    else:
        print('FALHA NA AUTENCAÇÃO!')
        break



    
                
    



        
