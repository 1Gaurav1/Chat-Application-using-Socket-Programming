import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NICK":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("[!] Disconnected from server.")
            client.close()
            break

def send_messages(client):
    while True:
        try:
            message = input("")
            if message.strip() == "":
                continue
            full_message = f"[{nickname}]: {message}"
            client.send(full_message.encode())
        except:
            break

# ---- MAIN ----
nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('localhost', 9999))
    print(f"Connected to server as '{nickname}'. Type to chat!\n")
except:
    print("[!] Could not connect to server. Make sure server.py is running.")
    exit()

# Two threads — one for receiving, one for sending
recv_thread = threading.Thread(target=receive_messages, args=(client,))
recv_thread.daemon = True
recv_thread.start()

send_messages(client)