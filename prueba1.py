#ARCHIVO DEFINITIVOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
import tkinter as tk
from tkinter import messagebox
import sqlite3
import pyotp
import qrcode
from PIL import Image, ImageTk
import io

class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("350x400")

        self.label_username = tk.Label(root, text="Nombre de Usuario:")
        self.label_password = tk.Label(root, text="Contraseña:")
        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")
        self.label_codigo_totp = tk.Label(root, text="Código TOTP:")
        self.entry_codigo_totp = tk.Entry(root)

        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.label_codigo_totp.pack()
        self.entry_codigo_totp.pack()
        self.btn_login.pack(pady=10)

    def iniciar_sesion(self):
        usuario = self.entry_username.get()
        contrasena = self.entry_password.get()
        codigo_totp_ingresado = self.entry_codigo_totp.get()

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT contrasena, claveAuthenticator FROM usuarios WHERE usuario = ?", (usuario,))
        registro = cursor.fetchone()
        conexion.close()

        if registro:
            contrasena_correcta = registro[0]
            clave_authenticator = registro[1]
            totp = pyotp.TOTP(clave_authenticator)

            if contrasena == contrasena_correcta and totp.verify(codigo_totp_ingresado):
                messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
            else:
                messagebox.showerror("Inicio de Sesión", "Usuario, contraseña o código TOTP incorrectos.")
        else:
            messagebox.showerror("Inicio de Sesión", "Usuario no encontrado.")

#####################################################################################################################

class VentanaRegistro:
    def __init__(self, root):
        actualizar_base_de_datos()
        self.root = root
        self.root.title("Registro")
        self.root.state('zoomed')

        self.label_username = tk.Label(root, text="Nombre de Usuario:")
        self.label_password = tk.Label(root, text="Contraseña:")
        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")
        self.btn_register = tk.Button(root, text="Registrar", command=self.registrar_usuario)

        self.secreto_totp = generar_secreto_totp()

        self.mostrar_qr(self.secreto_totp)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_register.pack(pady=10)

    def generar_nombre_usuario(self):
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(id) FROM usuarios")
        max_id = cursor.fetchone()[0]
        conexion.close()
    
        if max_id is None:
            max_id = 0
    
        nombre_usuario = f"{max_id}°USUARIO"
        return nombre_usuario

    def mostrar_qr(self, secreto):
        nombre_usuario = self.generar_nombre_usuario()
        qr = generarQR(nombre_usuario,secreto)

        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        
        qr_image = Image.open(qr_buffer)

        qr_photo = ImageTk.PhotoImage(qr_image)

        qr_label = tk.Label(self.root, image=qr_photo)
        qr_label.image = qr_photo 
        qr_label.pack()

    def registrar_usuario(self):
        usuario = self.entry_username.get()
        contrasena = self.entry_password.get()
        secreto = self.secreto_totp
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            # Asegúrate de ajustar el esquema de tu tabla 'usuarios' para incluir una columna para la clave TOTP
            cursor.execute("INSERT INTO usuarios (usuario, contrasena, claveAuthenticator) VALUES (?, ?, ?)", (usuario, contrasena, secreto))
            conexion.commit()
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registro", "El Usuario ya existe.")
        finally:
            conexion.close()

##################################################################################################################################################

class VentanaPrueba:
    def __init__(self, root):
        actualizar_base_de_datos()
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
        
        self.btn_verificar = tk.Button(root, text="Verificar Código", command=self.verificar_codigo)
        self.btn_verificar.pack(pady=20)

    def verificar_codigo(self):
        codigo_ingresado = self.entry_codigo.get()
        totp = pyotp.TOTP(self.valor_clave_authenticator)
        if totp.verify(codigo_ingresado):
            messagebox.showinfo("Verificación", "El código es correcto.")
        else:
            messagebox.showerror("Verificación", "NOOOOOOOOOOOOOOOOOOOO.")
        
#############################################################################################################################

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

##########################################################################################################################################

def conectar_db():
        return sqlite3.connect('Usuarios.db')

def actualizar_base_de_datos():
    conexion = sqlite3.connect('Usuarios.db')
    if conexion:
        conexion.commit()
        print("Base de Datos actualizada.")
    else:
        print("No hay una conexión activa a la base de datos.")

def generar_secreto_totp():
    secreto = pyotp.random_base32()
    return secreto

secreto_totp1 = generar_secreto_totp()
secreto_totp2 = generar_secreto_totp()
secreto_totp3 = generar_secreto_totp()
secreto_totp4 = generar_secreto_totp()
print("Secreto TOTP generado:", secreto_totp1)
print("Secreto TOTP generado:", secreto_totp2)
print("Secreto TOTP generado:", secreto_totp3)
print("Secreto TOTP generado:", secreto_totp4)

def generarQR(nombre, secreto):
    emisor = "Login Experimental"
    uri = pyotp.totp.TOTP(secreto).provisioning_uri(name=nombre, issuer_name=emisor)
    qr = qrcode.make(uri)
    
    print(f"Se generó el código QR para {nombre}.")
    return qr
    


root = tk.Tk()
app = PaginaInicial(root)
root.mainloop()


#archivo_qr = f"{nombre}_qr.png"
    #qr.save(archivo_qr)
    #img = Image.open(archivo_qr)
    #img.show()