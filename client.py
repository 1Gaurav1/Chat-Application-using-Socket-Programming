import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# GUI Colors - Modern Dark Theme
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#ffffff"
INPUT_BG = "#2d2d2d"
BTN_BG = "#007acc"
BTN_FG = "#ffffff"
BTN_ACTIVE = "#005999"
FONT = ("Segoe UI", 11)

class ChatApp:                       
    
    def __init__(self, root):                       
        
        self.root = root                       
        
        self.root.title("Chat Client")                       
        
        self.root.geometry("400x550")                       
        
        self.root.configure(bg=BG_COLOR)                       
        
            
            
        # Connection status                       
        
        self.client = None                       
        
        self.nickname = ""                       
        
            
            
        self.build_login_screen()                       
        
    
    
    def build_login_screen(self):
        self.login_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.login_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        title = tk.Label(self.login_frame, text="Welcome to Chat", font=("Segoe UI", 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        title.pack(pady=(0, 30))
        
        lbl_nick = tk.Label(self.login_frame, text="Enter your nickname:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
        lbl_nick.pack(anchor="w", pady=(0, 5))
        
        self.nick_entry = tk.Entry(self.login_frame, font=FONT, bg=INPUT_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.nick_entry.pack(fill=tk.X, pady=(0, 20))
        self.nick_entry.focus()
        
        lbl_ip = tk.Label(self.login_frame, text="Server IP:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
        lbl_ip.pack(anchor="w", pady=(0, 5))
        
        self.ip_entry = tk.Entry(self.login_frame, font=FONT, bg=INPUT_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.ip_entry.insert(0, "localhost")
        self.ip_entry.pack(fill=tk.X, pady=(0, 20))
        
        lbl_port = tk.Label(self.login_frame, text="Server Port:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
        lbl_port.pack(anchor="w", pady=(0, 5))
        
        self.port_entry = tk.Entry(self.login_frame, font=FONT, bg=INPUT_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.port_entry.insert(0, "9999")
        self.port_entry.pack(fill=tk.X, pady=(0, 30))
        
        connect_btn = tk.Button(self.login_frame, text="Connect", font=("Segoe UI", 12, "bold"), bg=BTN_BG, fg=BTN_FG, 
                                activebackground=BTN_ACTIVE, activeforeground=BTN_FG, relief=tk.FLAT, cursor="hand2", command=self.connect_to_server)
        connect_btn.pack(fill=tk.X, ipady=10)

        # Bind Enter key to connect
        self.root.bind("<Return>", lambda event: self.connect_to_server())

    def connect_to_server(self):
        self.nickname = self.nick_entry.get().strip()
        ip = self.ip_entry.get().strip()
        port_str = self.port_entry.get().strip()
        
        if not self.nickname:
            messagebox.showerror("Error", "Nickname cannot be empty!")
            return
            
        try:
            port = int(port_str)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, port))
            
            # Setup successful
            self.root.unbind("<Return>")
            self.login_frame.destroy()
            self.build_chat_screen()
            
            # Start receive thread
            recv_thread = threading.Thread(target=self.receive_messages)
            recv_thread.daemon = True
            recv_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Port must be an integer!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to {ip}:{port_str}.\nEnsure server is running.\n\nError: {str(e)}")

    def build_chat_screen(self):
        self.chat_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.chat_frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header = tk.Frame(self.chat_frame, bg=INPUT_BG, height=50)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        lbl_user = tk.Label(header, text=f"Logged in as: {self.nickname}", font=("Segoe UI", 11, "bold"), bg=INPUT_BG, fg=TEXT_COLOR)
        lbl_user.pack(side=tk.LEFT, padx=15)
        
        # Input Area (MUST BE PACKED BEFORE THE EXPANDING CHAT AREA)
        input_frame = tk.Frame(self.chat_frame, bg=BG_COLOR)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 10))
        
        self.msg_entry = tk.Entry(input_frame, font=FONT, bg=INPUT_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.msg_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=8, padx=(0, 10))
        self.msg_entry.focus()
        
        send_btn = tk.Button(input_frame, text="Send", font=("Segoe UI", 11, "bold"), bg=BTN_BG, fg=BTN_FG, 
                             activebackground=BTN_ACTIVE, activeforeground=BTN_FG, relief=tk.FLAT, cursor="hand2", command=self.send_message)
        send_btn.pack(side=tk.RIGHT, ipadx=15, ipady=8)
        
        # Bind Enter key to send message
        self.root.bind("<Return>", lambda event: self.send_message())

        # Chat Display (Expands to fill remaining vertical space)
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT,
                                                  state=tk.DISABLED, padx=10, pady=10, relief=tk.FLAT, selectbackground="#4d4d4d")
        self.chat_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Configure text tags for basic colors
        self.chat_area.tag_configure("server", foreground="#00cc66")
        self.chat_area.tag_configure("me", foreground="#00aaff")
        self.chat_area.tag_configure("other", foreground="#ffb84d")

        self.display_message("[+] Connected to server! Start chatting.", tag="server")

    def display_message(self, message, tag=None):
        self.chat_area.config(state=tk.NORMAL)
        if tag:
            self.chat_area.insert(tk.END, message + "\n", tag)
        else:
            self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message == "NICK":
                    self.client.send(self.nickname.encode())
                else:
                    tag = None
                    if message.startswith("[SERVER]"):
                        tag = "server"
                    else:
                        tag = "other"
                    self.root.after(0, self.display_message, message, tag)
            except:
                self.root.after(0, self.display_message, "[!] Disconnected from server.", "server")
                if self.client:
                    try:
                        self.client.close()
                    except:
                        pass
                break

    def send_message(self):
        message = self.msg_entry.get()
        if message.strip():
            try:
                full_message = f"[{self.nickname}]: {message}"
                self.client.send(full_message.encode())
                
                # Directly display our own message locally
                self.display_message(full_message, tag="me")
                
                self.msg_entry.delete(0, tk.END)
            except:
                self.display_message("[!] Error sending message. Server may be down.", tag="server")

    def on_closing(self):
        if self.client:
            try:
                self.client.close()
            except:
                pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()