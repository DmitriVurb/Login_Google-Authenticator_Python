import tkinter as tk
from tkinter import messagebox
import sqlite3
import pyotp
import qrcode
from PIL import Image, ImageTk
import io

def conectar_db():
        return sqlite3.connect('Usuarios.db')

usuario = "admin1"
conexion = conectar_db()
cursor = conexion.cursor()
cursor.execute("SELECT claveAuthenticator FROM usuarios WHERE usuario = ?", (usuario,))
registro = cursor.fetchone()
conexion.close()


valor_clave_authenticator = registro[0]

print("Clave en la base de datos:", valor_clave_authenticator)