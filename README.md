# 💬 Chat Application using Socket Programming

A multi-client terminal-based chat application built with Python using **TCP Socket Programming** and **Threading**. Built as part of the Computer Networks (INT3201) course project.

---

## 📌 Features

- Multi-client support (multiple users can chat simultaneously)
- Nickname system for each user
- Join/leave notifications broadcast to all users
- Messages broadcast to all connected clients
- Threaded server — no blocking, handles multiple clients smoothly
- Clean disconnect handling

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| Protocol | TCP (Transmission Control Protocol) |
| Library | `socket`, `threading` (built-in) |
| Architecture | Client-Server Model |

---

## 📁 Project Structure

```
chat-application/
│
├── server.py       # Server-side code (run this first)
├── client.py       # Client-side code (run one per user)
└── README.md
```

---

## ⚙️ How to Run

### Prerequisites
- Python 3.x installed
- No external libraries needed (uses built-in modules only)

### Step 1 — Start the Server
Open a terminal and run:
```bash
python server.py
```
You should see:
```
========================================
  Server started on port 9999
  Waiting for connections...
========================================
```

### Step 2 — Connect Clients
Open **2 or more terminals** and run in each:
```bash
python client.py
```
Enter a nickname when prompted and start chatting!

---

## 🖥️ Demo

```
Terminal 1 (Server):
  Server started on port 9999
  [+] Alice connected from ('127.0.0.1', 52341)
  [+] Bob connected from ('127.0.0.1', 52342)
  [Alice]: Hey Bob!
  [Bob]: Hello Alice!

Terminal 2 (Client - Alice):
  Enter your nickname: Alice
  Connected to server as 'Alice'. Type to chat!
  [SERVER] Bob joined the chat!
  Hey Bob!
  [Bob]: Hello Alice!

Terminal 3 (Client - Bob):
  Enter your nickname: Bob
  Connected to server as 'Bob'. Type to chat!
  [Alice]: Hey Bob!
  Hello Alice!
```

---

## 🔑 Key Concepts Used

| Concept | Description |
|---|---|
| **Socket** | Endpoint for communication, defined by IP + Port |
| **TCP** | Reliable, ordered, connection-based protocol |
| **`bind()`** | Attaches socket to IP and port |
| **`listen()`** | Puts server in passive mode to accept connections |
| **`accept()`** | Accepts incoming client connection |
| **`threading`** | Handles multiple clients concurrently |
| **`broadcast()`** | Sends message from one client to all others |
| **`AF_INET`** | IPv4 address family |
| **`SOCK_STREAM`** | TCP socket type |

---

## 📊 Architecture

```
                    ┌─────────────┐
                    │   SERVER    │
                    │  Port 9999  │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼─────┐  ┌──────▼─────┐  ┌──────▼─────┐
    │  Client 1  │  │  Client 2  │  │  Client 3  │
    │   (Alice)  │  │   (Bob)    │  │  (Charlie) │
    └────────────┘  └────────────┘  └────────────┘
```

When a client sends a message → Server receives it → Broadcasts to **all other clients**

---

## 🔒 Limitations

- No message encryption (plain text)
- No persistent message history
- Runs on localhost by default (can be changed to a public IP)
- No GUI (terminal-based only)

---

## 🚀 Possible Improvements

- [ ] Add SSL/TLS encryption for secure messaging
- [ ] Build a GUI using `tkinter` or a web interface
- [ ] Add private messaging between users
- [ ] Store chat history in a database
- [ ] Deploy on a cloud server for internet-based chatting

---

## 👨‍💻 Author

**Gaurav**
B.Tech — Information Technology
MUJ Manipal University Jaipur
Course: Computer Networks (INT3201)

---

## 📄 License

This project is for educational purposes as part of a university course assignment.
