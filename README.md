# 💬 Messagerie instantanée Privé en Python (Client-Serveur)

Ce projet est une application simple de messagerie en ligne de commande entre deux clients, via un serveur Python. Elle peut être utilisée en local ou sur un réseau local (LAN).  

Elle utilise d'abord un chiffrement asymétrique RSA pour un échange de clés AES, puis chiffre les messages en utilisant le chiffrement symétrique AES.

---

## 📦 Prérequis

- Python 3.x installé
- pip install cryptography-suite

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
&emsp;🖥️ En local (localhost)  

&emsp;&emsp;Lancez client.py dans deux terminaux différents sur la même machine :  

&emsp;&emsp;bash  

&emsp;&emsp;Copier  

&emsp;&emsp;Modifier  

&emsp;&emsp;python client.py    

&emsp;🌐 En réseau local (LAN)  
&emsp;&emsp;Récupérer l'adresse IPv4 de la machine sur laquelle tourne server.py :  

&emsp;&emsp;Sous Windows : ipconfig  
&emsp;&emsp;Sous Unix-like / macOS :  ifconfig 

&emsp;Modifier le fichier client.py :  

&emsp;&emsp;Remplacez l’adresse IP (à la ligne 10) par celle de la machine qui exécute le serveur.  

### 🧑‍🤝‍🧑 Étape 3 : Choisir les pseudos
Chaque client doit entrer un pseudo unique.

Par exemple :

Client 1 : Alice

Client 2 : Bob

### 🔒 Étape 4 : Démarrer une session privée
Le client Alice envoie une demande de session privée a Bob :

```/private Bob```  

Le client Alice accepte la session en répondant :

```/private Alice```  

Une fois la connexion établie, la communication est privée entre les deux clients.

# 📁 Fichiers du projet
server.py : serveur principal

client.py : client à exécuter dans chaque terminal
