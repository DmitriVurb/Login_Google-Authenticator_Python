class VentanaRegistro:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro")
        self.root.geometry("350x400")

        self.label_username = tk.Label(root, text="Nombre de Usuario:")
        self.entry_username = tk.Entry(root)
        self.label_password = tk.Label(root, text="Contraseña:")
        self.entry_password = tk.Entry(root, show="*")
        self.btn_register = tk.Button(root, text="Registrar", command=self.registrar_usuario)
        
        # Genera una clave secreta TOTP para el nuevo usuario
        self.secreto_totp = pyotp.random_base32()
        # Genera y muestra el código QR para esta clave secreta
        self.mostrar_qr(self.secreto_totp)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_register.pack(pady=10)

    def mostrar_qr(self, secreto):
        emisor = "Login Experimental"
        nombre = "Temporal"  # Este valor es solo un placeholder
        uri = pyotp.totp.TOTP(secreto).provisioning_uri(name=nombre, issuer_name=emisor)
        qr = qrcode.make(uri)
        
        # Convierte el QR en una imagen que se pueda mostrar en Tkinter
        qr_image = Image.open(io.BytesIO(qr.png(le=10, quiet_zone=1)))
        qr_photo = ImageTk.PhotoImage(qr_image)
        qr_label = tk.Label(self.root, image=qr_photo)
        qr_label.image = qr_photo  # Mantener una referencia.
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
            messagebox.showinfo("Registro", "Usuario registrado exitosamente. Escanea el código QR con tu app de autenticación.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registro", "El nombre de usuario ya existe.")
        finally:
            conexion.close()
