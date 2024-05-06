import tkinter as tk
from tkinter import messagebox

class PaginaInicial:
    def __init__(self,root):
        self.root = root
        self.root.title("Inicio")
        self.root.geometry("350x400") 

class RegistroVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio")
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
        self.btn_register.pack(padx=20, pady=20)

    def registrar_usuario(self):
        # Aquí puedes agregar la lógica para registrar al usuario en la base de datos
        messagebox.showinfo("Registro", "Usuario registrado exitosamente.")

class LoginVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.label_username = tk.Label(root, text="Nombre de Usuario:")
        self.label_password = tk.Label(root, text="Contraseña:")
        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")
        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_login.pack(padx=20, pady=20)

    def iniciar_sesion(self):
        # Aquí puedes agregar la lógica para verificar la autenticación en la base de datos
        messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")

# Crear la aplicación
root = tk.Tk()

# Crear instancias de las ventanas
pagina_inicial = PaginaInicial(root)
#registro_ventana = RegistroVentana(root)
#login_ventana = LoginVentana(root)

# Mostrar la ventana principal
root.mainloop()
