import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configurações de Rede (IPv6)
HOST = '::1'  # Localhost IPv6
PORT = 50007

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor de Teste - Monitoramento (IPv6)")
        self.root.geometry("600x400")
        
        # Interface Gráfica
        tk.Label(root, text="Log de Teclas Recebidas (Keylogger Server)", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.log_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.log_area.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Status: Parado", fg="red")
        self.status_label.pack()

        self.btn_start = tk.Button(root, text="Iniciar Servidor IPv6", command=self.start_server, bg="green", fg="white")
        self.btn_start.pack(pady=5)

        self.server_socket = None
        self.running = False

    def start_server(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(1)
            self.status_label.config(text=f"Escutando em {HOST}::{PORT}", fg="blue")
            self.update_log(f"Servidor iniciado. Aguardando conexão IPv6...\n")
            
            # Thread para não travar a interface
            threading.Thread(target=self.accept_connections, daemon=True).start()
            self.btn_start.config(state="disabled")
        except Exception as e:
            self.update_log(f"Erro ao iniciar: {e}\n")

    def accept_connections(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                self.update_log(f"Conectado por: {addr}\n")
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
            except:
                break

    def handle_client(self, conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Decodifica e mostra no log
                msg = data.decode('utf-8')
                self.update_log(f"{msg}")

    def update_log(self, message):
        self.log_area.insert(tk.END, message)
        self.log_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()