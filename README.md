# 💬 Chat Privé en Python (Client-Serveur)

Ce projet est une application simple de messagerie en ligne de commande entre deux clients, via un serveur Python. Elle peut être utilisée en local ou sur un réseau local (LAN).
Elle utilise d'abord un chiffrement asymetrique RSA pour un échange de clés AES, puis chiffre les messages en utilisant le chiffrement symetrique AES

---

## 📦 Prérequis

- Python 3.x installé
- Aucune bibliothèque externe nécessaire (tout est basé sur la bibliothèque standard)

---
## 📁 Fichiers du projet
    server.py : serveur principal

    client.py : client à exécuter dans chaque terminal

## 🚀 Instructions d'utilisation

### 🧩 Étape 1 : Lancer le serveur

Dans un terminal, exécutez le fichier `server.py` :

```bash
python server.py 
```
### 💻 Étape 2 : Lancer les clients
🖥️ En local (localhost)
Lancez client.py dans deux terminaux différents sur la même machine :

bash
Copier
Modifier
python client.py
🌐 En réseau local (LAN)
Récupérer l'adresse IPv4 de la machine sur laquelle tourne server.py :

Sous Windows :

bash
Copier
Modifier
ipconfig
Sous Unix-like / macOS :

bash
Copier
Modifier
ifconfig
Modifier le fichier client.py :

Remplacez l’adresse IP (à la ligne 10) par celle de la machine qui exécute le serveur.

### 🧑‍🤝‍🧑 Étape 3 : Choisir les pseudos
Chaque client doit entrer un pseudo unique.

Par exemple :

Client 1 : Nom_A

Client 2 : Nom_B

### 🔒 Étape 4 : Démarrer une session privée
Le client Nom_A envoie une demande de session privée :

arduino
Copier
Modifier
/private Nom_B
Le client Nom_B accepte la session en répondant :

arduino
Copier
Modifier
/private Nom_A
Une fois la connexion établie, la communication est privée entre les deux clients.

# 📁 Fichiers du projet
server.py : serveur principal

client.py : client à exécuter dans chaque terminal
