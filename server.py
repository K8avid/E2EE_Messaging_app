import socket
import select


class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.buffer_size = 1024
        #SOCK_STREAM = TCD, SOCK_DGRAM = UDP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.server_socket.setblocking(False)

        self.epoll = select.epoll()
        self.epoll.register(self.server_socket.fileno(), select.EPOLLIN)

        self.connections = {}       # fd → socket
        self.pseudos = {}           # fd → pseudo
        self.pseudo_to_fd = {}      # pseudo → fd
        self.private_sessions = {}  # pseudo → pseudo

    def run(self):
        print(f"Serveur actif sur {self.host}:{self.port}")
        try:
            while True:
                for fileno, event in self.epoll.poll(1):
                    if fileno == self.server_socket.fileno():
                        self.handle_new_connection()
                    elif event & select.EPOLLIN:
                        self.handle_client_message(fileno)
        finally:
            self.epoll.unregister(self.server_socket.fileno())
            self.epoll.close()
            self.server_socket.close()

    def handle_new_connection(self):
        client_socket, _ = self.server_socket.accept()
        client_socket.setblocking(False)
        self.epoll.register(client_socket.fileno(), select.EPOLLIN)
        self.connections[client_socket.fileno()] = client_socket
        client_socket.sendall("[Server]Choisis un pseudo: ".encode())

    def handle_client_message(self, fileno):
        sock = self.connections.get(fileno)
        if not sock:
            return

        try:
            data = sock.recv(self.buffer_size)
            if not data:
                raise ConnectionResetError
            try:
                msg = data.decode().strip()
            except UnicodeDecodeError:
                 sender = self.pseudos[fileno]
                 self.send_AES_key(sender,data)
                 return
            
            msg = data.decode().strip()
            if fileno not in self.pseudos:
                pseudo = msg
                if pseudo in self.pseudo_to_fd:
                    sock.sendall("[Server] Pseudo déjà pris. Déconnexion.\n".encode())
                    self.close_connection(fileno)
                else:
                    self.pseudos[fileno] = pseudo
                    self.pseudo_to_fd[pseudo] = fileno
                    sock.sendall("[Server] Bienvenue ! Utilise /private <pseudo> pour discuter.\n".encode())
                    print(f"[Connexion] {pseudo}")
                return

            sender = self.pseudos[fileno]
            if msg.startswith("/private "):
                self.process_command(sender, msg)
            else:
                self.send_private_message(sender, msg)

        except ConnectionResetError:
            self.close_connection(fileno)

    def process_command(self, sender, msg):
        parts = msg.split(" ", 1)
        if len(parts) != 2:
            self.send(sender, "[Server] Utilise : /private <pseudo>\n")
            return

        target = parts[1]
        if target == sender:
            self.send(sender, "[Server] Tu ne peux pas te parler à toi-même...\n")
            return

        if target not in self.pseudo_to_fd:
            self.send(sender, f"[Server] {target}[Server] n'est pas connecté.\n")
            return

        # Si les deux ont déjà confirmé
        if self.private_sessions.get(sender) == target and self.private_sessions.get(target) == sender:
            self.send(sender, f"[Server] Tu as initié une session privée avec {target} !\n")
            self.send(target, f"[Server] Tu as accepté une session privée avec {sender} !\n")
            return

        # Si target a déjà demandé une session avec sender → confirmation mutuelle
        if self.private_sessions.get(target) == sender:
            self.private_sessions[sender] = target
            self.send(sender, f"[Server] Tu as accepté une session privée avec {target} !\n")
            self.send(target, f"[Server] Tu as initié une session privée avec {sender} !\n")
        else:
            # Première demande
            self.private_sessions[sender] = target
            self.send(sender, f"[Server] Tu as demandé une session avec {target}. En attente de confirmation...\n")
            self.send(target, f"[Server] {sender} veut discuter en privé. Tape /private {sender} pour accepter.\n")

    def send_private_message(self, sender, msg):
        target = self.private_sessions.get(sender)

        if target and self.private_sessions.get(target) == sender:
            if target in self.pseudo_to_fd:
                target_fd = self.pseudo_to_fd[target]
                # self.send_fd(target_fd, f"[Privé] {sender} : {msg}\n")
                self.send_fd(target_fd, f"{msg}\n")
            else:
                self.send(sender, f"[Server] {target} n'est plus connecté.\n")
        else:
            self.send(sender, "[Server] Pas de session privée active. Utilise /private <pseudo>.\n")

    def send_AES_key(self, sender, msg):
        target = self.private_sessions.get(sender)
        if target and self.private_sessions.get(target) == sender:
            if target in self.pseudo_to_fd:
                target_fd = self.pseudo_to_fd[target]
                self.send_fd_AES(target_fd, msg)
            else:
                self.send(sender, f"[Server] {target} n'est plus connecté.\n")


    def send(self, pseudo, msg):
        fd = self.pseudo_to_fd.get(pseudo)
        if fd:
            self.send_fd(fd, msg)

    def send_fd(self, fileno, msg):
        sock = self.connections.get(fileno)
        if sock:
            sock.sendall(msg.encode())

    def send_fd_AES(self, fileno, msg):
        sock = self.connections.get(fileno)
        if sock:
            sock.sendall(msg)

    def close_connection(self, fileno):
        pseudo = self.pseudos.get(fileno, "inconnu")
        print(f"[Déconnexion] {pseudo}")
        self.epoll.unregister(fileno)
        sock = self.connections.pop(fileno, None)
        if sock:
            sock.close()
        if fileno in self.pseudos:
            pseudo_str = self.pseudos.pop(fileno)
            self.pseudo_to_fd.pop(pseudo_str, None)
            self.private_sessions = {
                k: v for k, v in self.private_sessions.items()
                if k != pseudo_str and v != pseudo_str
            }

if __name__ == "__main__":
    server = Server()
    server.run()
