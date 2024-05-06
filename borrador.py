import tkinter as tk
from tkinter import messagebox
import sqlite3
import pyotp

class VentanaLogin:
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
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (self.entry_username.get(),))
        registro = cursor.fetchone()
        conexion.close()

        if registro and self.entry_password.get() == registro[0]:
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
        else:
            messagebox.showerror("Inicio de Sesión", "Usuario o contraseña incorrectos.")



class VentanaRegistro:
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
        conexion = conectar_db()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (self.entry_username.get(), self.entry_password.get()))
            conexion.commit()
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registro", "El nombre de usuario ya existe.")
        finally:
            conexion.close()

class VentanaPrueba:
    def __init__(self, root):
        self.root = root
        self.root.title("Prueba Autenticador")
        self.root.geometry("350x400")

        self.label_codigo = tk.Label(root, text="Código Autenticador:")
        self.entry_codigo = tk.Entry(root)
        self.label_codigo.pack()
        self.entry_codigo.pack()

        usuario = "prueba"
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT claveAuthenticator FROM usuarios WHERE usuario = ?", (usuario,))
        registro = cursor.fetchone()
        conexion.close()
        
        self.valor_clave_authenticator = registro[0]
        
        print("Clave en la base de datos:", self.valor_clave_authenticator)
        
        self.btn_verificar = tk.Button(root, text="Verificar Código", command=lambda: self.verificar_codigo())
        self.btn_verificar.pack(pady=20)

    def verificar_codigo(self):
        codigo_ingresado = self.entry_codigo.get()
        if self.valor_clave_authenticator and codigo_ingresado == self.valor_clave_authenticator:
            messagebox.showinfo("Verificación", "El código es correcto.")
        else:
            messagebox.showerror("Verificación", "El código es incorrecto.")
        

class PaginaInicial:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio")
        self.root.geometry("350x400")

        self.btn_iniciar_sesion = tk.Button(root, text="Iniciar Sesión", command=self.abrir_ventana_login)
        self.btn_crear_usuario = tk.Button(root, text="Crear Usuario", command=self.abrir_ventana_registro)
        self.btn_probar_autenticador = tk.Button(root, text="Probar Autenticador", command=self.abrir_ventana_prueba)

        self.btn_iniciar_sesion.pack(pady=20)
        self.btn_crear_usuario.pack(pady=20)
        self.btn_probar_autenticador.pack(pady=20)

    def abrir_ventana_login(self):
        self.root.withdraw()  
        ventana_login = tk.Toplevel()
        app_login = VentanaLogin(ventana_login)
        ventana_login.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(ventana_login))

    def abrir_ventana_registro(self):
        self.root.withdraw()  
        ventana_registro = tk.Toplevel()
        app_registro = VentanaRegistro(ventana_registro)
        ventana_registro.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(ventana_registro))

    def abrir_ventana_prueba(self):
        self.root.withdraw()  
        ventana_prueba = tk.Toplevel()
        app_prueba = VentanaPrueba(ventana_prueba)
        ventana_prueba.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(ventana_prueba))

    def cerrar_ventana(self, ventana_secundaria):
        ventana_secundaria.destroy()
        self.root.deiconify() 

def conectar_db():
        return sqlite3.connect('Usuarios.db')


root = tk.Tk()
app = PaginaInicial(root)
root.mainloop()

