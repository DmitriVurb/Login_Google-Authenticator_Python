import tkinter as tk
from tkinter import messagebox
import sqlite3
import pyotp
import qrcode
from PIL import Image, ImageTk
import io

def generar_secreto_totp():
    secreto = pyotp.random_base32()
    return secreto

secreto_totp1 = "PDNIASUFHBAS3872CTLBSR7IH4MQQQIX"
print("Secreto TOTP generado:", secreto_totp1)

nombre_prueba = "ADMIN_prov"

def generarQR(nombre, secreto):
    emisor = "Login Experimental"
    uri = pyotp.totp.TOTP(secreto).provisioning_uri(name=nombre, issuer_name=emisor)
    qr = qrcode.make(uri)
    archivo_qr = f"{nombre}_qr.png"
    qr.save(archivo_qr)
    img = Image.open(archivo_qr)
    img.show()
    print(f"Se generó el código QR para {nombre}.")
    return qr

generarQR(nombre_prueba, secreto_totp1)

