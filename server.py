import socket
import threading

clients = []
nicknames = []

def broadcast(message, sender_conn=None):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        broadcast(f"[SERVER] {nickname} left the chat.".encode())
        client.close()

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, sender_conn=client)
            print(message.decode())
        except:
            break
    remove_client(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("=" * 40)
    print("  Server started on port 9999")
    print("  Waiting for connections...")
    print("=" * 40)

    while True:
        client, address = server.accept()

        # Ask for nickname
        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print(f"[+] {nickname} connected from {address}")
        broadcast(f"[SERVER] {nickname} joined the chat!".encode())
        client.send("[SERVER] You are connected! Start chatting.\n".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

start_server()