import tkinter as tk
from tkinter import messagebox

class PaginaInicial:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio")
        self.root.geometry("350x400") 

        # Botón para abrir la ventana de registro
        self.btn_open_registro = tk.Button(root, text="Registrar Usuario", command=self.abrir_registro)
        self.btn_open_registro.pack(pady=10)

        # Botón para abrir la ventana de login
        self.btn_open_login = tk.Button(root, text="Iniciar Sesión", command=self.abrir_login)
        self.btn_open_login.pack(pady=10)

    def abrir_registro(self):
        # Abre la ventana de registro
        self.registro_ventana = RegistroVentana(tk.Toplevel(self.root))

    def abrir_login(self):
        # Abre la ventana de login
        self.login_ventana = LoginVentana(tk.Toplevel(self.root))

class RegistroVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro")
        self.root.geometry("350x400")

        self.label_username = tk.Label(root, text="Nombre de Usuario:")
        self.label_password = tk.Label(root, text="Contraseña:")
        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")
        self.btn_register = tk.Button(root, text="Registrar", command=self.registrar_usuario)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_register.pack(pady=10)

    def registrar_usuario(self):
        # Aquí puedes agregar la lógica para registrar al usuario en la base de datos
        messagebox.showinfo("Registro", "Usuario registrado exitosamente.")

class LoginVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("350x400")

        self.label_username = tk.Label(root, text="Nombre de Usuario:")
        self.label_password = tk.Label(root, text="Contraseña:")
        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")
        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_login.pack(pady=10)

    def iniciar_sesion(self):
        # Aquí puedes agregar la lógica para verificar la autenticación en la base de datos
        messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")

# Crear la aplicación
root = tk.Tk()

# Crear instancia de la página inicial
pagina_inicial = PaginaInicial(root)

# Mostrar la ventana principal
root.mainloop()
