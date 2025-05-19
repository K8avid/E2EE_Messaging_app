import socket
import select
import sys

from cryptography_suite.asymmetric import generate_rsa_keypair, rsa_encrypt, rsa_decrypt, serialize_public_key,  load_public_key
from cryptography_suite.encryption import aes_encrypt, aes_decrypt

#======= Rentrer l'adresse IP de la machine du serveur ici ! =======
HOST = '127.0.0.1'
#===================================================================

PORT = 12345
BUFFER_SIZE = 1024
KEY_SIZE = 4096
FORMAT = 'utf-8'
HEADER = 64

class PrivateChatClient:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.buffer_size = BUFFER_SIZE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session_started = False
        self.is_initiator = False
        self.aes_key = 0
        self.rsa_pub = 0
        self.rsa_priv = 0
        self.pseudo = "None"

    def start(self):
        self.sock.connect((self.host, self.port))
        print(self.sock.recv(self.buffer_size).decode(), end='')  # Choisis un pseudo: 
        self.pseudo = input()
        self.sock.sendall(self.pseudo.encode())
        try:
            while True:
                readable, _, _ = select.select([sys.stdin, self.sock], [], [])
                for source in readable:
                    if source == self.sock:

                        self.recv_decode_handle()

                    else:

                        self.encode_send()

        except KeyboardInterrupt:
            print("\nDéconnexion...")
        finally:
            self.sock.close()

    def attribution_role(self, message):
        #print(f"handle_seesion: {message}, session_started = {self.session_started}")
        if not self.session_started and "session privée avec" in message:
            self.session_started = True
            if "Tu as initié" in message:
                self.is_initiator = True
            if self.is_initiator:
                self.first()
            else:
                self.second()
    
            

    def first(self): #1er evoie RSA public, puis recupere la clé AES de 2e qui l'a chiffré avec RSA
        print("first est lancé")
        self.rsa_priv, self.rsa_pub = generate_rsa_keypair()
        serialized_rsa_pub = serialize_public_key(self.rsa_pub)
        # print(serialized_rsa_pub)
        self.sock.sendall(serialized_rsa_pub)

        ######## recuperer AES et dechiffrer ##########
        data = self.sock.recv(BUFFER_SIZE)
        #print(data)
        self.aes_key = rsa_decrypt(data,self.rsa_priv).decode(FORMAT)
        #print(f"[{self.aes_key}]")


    def second(self): #2e recupere RSA public, envoie AES chiffrer avec RSA,

        ############## reçoit RSA public ##############"   
        print("second est lancé")
        data = extract_public_key(self.sock.recv(KEY_SIZE))
        # print(data)
        self.rsa_pub = load_public_key(data)
        # print(rsa_key)

        ############## creer AES chiffré et envoie ####################
        self.aes_key = "AES_password"
        #print(self.aes_key)
        password_encrypted = rsa_encrypt(self.aes_key.encode(FORMAT), self.rsa_pub)
        #print(password_encrypted)
        self.sock.sendall(password_encrypted)
        #print(f"[{self.aes_key}]")

    def encode_send(self):
        user_input = sys.stdin.readline()
        if user_input:
            result = ""
            if user_input.startswith("/private "):
                result = user_input.strip()
            else:
                result = f"[Privé]{self.pseudo}: " + user_input
                result = aes_encrypt(result, self.aes_key)
                print(f"encoded messaged = [{result}]")
                
            self.sock.sendall(result.encode())

    def recv_decode_handle(self):

        data = self.sock.recv(self.buffer_size)
        if not data:
            print("🔌 Déconnecté du serveur.")
            return
        message = data.decode()
        if not message.startswith("/private") and "[Server]" not in message:
            message = aes_decrypt(message,self.aes_key)
        print(message, end='')

        self.attribution_role(message)
        

def extract_public_key(received_data):
    start_marker = b'-----BEGIN PUBLIC KEY-----'
    end_marker = b'-----END PUBLIC KEY-----'
    
    start = received_data.find(start_marker)
    end = received_data.find(end_marker) + len(end_marker)
    
    if start != -1 and end != -1:
        return received_data[start:end] + b'\n'
    return None


if __name__ == "__main__":
    client = PrivateChatClient()
    client.start()
