import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario
from models.cliente import Cliente
from ui.cliente import ClientePanel
from ui.admin_ui import AdminPanel
from auth import SesionActual
from utils import set_theme, toggle_theme, validar_email, validar_usuario

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.is_register = False
        self.setup_ui()

    def setup_ui(self):
      
        self.root.title("🔐 Iniciar Sesión - GymForTheMoment")
        self.root.geometry("420x580")
        
       
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

       
        ttk.Label(self.main_frame, text="🏋️ GymForTheMoment", 
                  style='Header.TLabel').pack(pady=(0, 10))
        ttk.Label(self.main_frame, text="Tu gimnasio, disponible 24/7", 
                  style='Sub.TLabel').pack(pady=(0, 30))

        self.create_login_fields()
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=20)
        
        self.login_btn = ttk.Button(btn_frame, text="🔐 Iniciar Sesión", command=self.login)
        self.login_btn.pack(side="left", padx=5)
        
        self.toggle_btn = ttk.Button(btn_frame, text="✏️ Crear Cuenta", command=self.toggle_mode)
        self.toggle_btn.pack(side="left", padx=5)
        
       
        theme_btn = ttk.Button(self.main_frame, text="🌓 Cambiar tema", 
                               command=lambda: toggle_theme(self.root), width=15)
        theme_btn.pack(pady=(10, 0))

    def create_login_fields(self):
      
        ttk.Label(self.main_frame, text="Usuario:").pack(anchor="w")
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.main_frame, textvariable=self.username_var, width=30)
        self.username_entry.pack(pady=(0, 10))
        self.username_var.trace("w", self.validate_username)

       
        ttk.Label(self.main_frame, text="Contraseña:").pack(anchor="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.main_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.pack(pady=(0, 20))
        self.password_var.trace("w", self.validate_password)
       
        self.password_entry.bind("<Return>", lambda e: self.login())

        self.user_feedback = ttk.Label(self.main_frame, text="", foreground="#7F8C8D")
        self.user_feedback.pack(anchor="w")
        self.pass_feedback = ttk.Label(self.main_frame, text="", foreground="#7F8C8D")
        self.pass_feedback.pack(anchor="w")

    def create_register_fields(self):
       
        for widget in self.main_frame.winfo_children():
            if widget not in [self.main_frame.winfo_children()[0], self.main_frame.winfo_children()[1]]:
                widget.destroy()

      
        ttk.Label(self.main_frame, text="📝 Registro de Cliente", 
                  style='Header.TLabel').pack(pady=(0, 10))
        ttk.Label(self.main_frame, text="Completa tus datos", 
                  style='Sub.TLabel').pack(pady=(0, 20))

        fields = [
            ("Nombre:", "name_var"),
            ("Email:", "email_var"),
            ("Teléfono:", "phone_var"),
            ("Usuario:", "username_var"),
            ("Contraseña:", "password_var")
        ]
        
        self.entries = {}
        for label_text, var_name in fields:
            ttk.Label(self.main_frame, text=label_text).pack(anchor="w")
            var = tk.StringVar()
       
            if var_name == "password_var":
                entry = ttk.Entry(self.main_frame, textvariable=var, show="*", width=30)
            else:
                entry = ttk.Entry(self.main_frame, textvariable=var, width=30)
            entry.pack(pady=(0, 8))
            self.entries[var_name] = (var, entry)
            
            if var_name == "password_var":
                entry.bind("<Return>", lambda e: self.register())
            
            if var_name == "email_var":
                var.trace("w", lambda *args, v=var: self.validate_email_field(v))
            elif var_name == "username_var":
                var.trace("w", lambda *args, v=var: self.validate_username_field(v))

        self.email_feedback = ttk.Label(self.main_frame, text="", foreground="#7F8C8D")
        self.email_feedback.pack(anchor="w", pady=(0,5))
        self.user_feedback_reg = ttk.Label(self.main_frame, text="", foreground="#7F8C8D")
        self.user_feedback_reg.pack(anchor="w", pady=(0,15))

        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="✅ Registrar", command=self.register).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="← Volver", command=self.toggle_mode).pack(side="left", padx=5)

    def validate_username(self, *args):
        user = self.username_var.get().strip()
        if user and not validar_usuario(user):
            self.user_feedback.config(text="❌ Mín. 3 caracteres, solo letras/números/guiones", foreground="#E74C3C")
        else:
            self.user_feedback.config(text="✅", foreground="#2ECC71") if user else self.user_feedback.config(text="")

    def validate_username_field(self, var):
        user = var.get().strip()
        label = self.user_feedback_reg
        if user and not validar_usuario(user):
            label.config(text="❌ Mín. 3 caracteres, solo letras/números", foreground="#E74C3C")
        else:
            label.config(text="✅", foreground="#2ECC71") if user else label.config(text="")

    def validate_email_field(self, var):
        email = var.get().strip()
        label = self.email_feedback
        if email and not validar_email(email):
            label.config(text="❌ Formato inválido (ej: user@email.com)", foreground="#E74C3C")
        else:
            label.config(text="✅", foreground="#2ECC71") if email else label.config(text="")

    def validate_password(self, *args):
        pwd = self.password_var.get()
        if pwd and len(pwd) < 4:
            self.pass_feedback.config(text="❌ Mínimo 4 caracteres", foreground="#E74C3C")
        else:
            self.pass_feedback.config(text="")

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showwarning("⚠️", "Complete todos los campos.")
            return

        user = Usuario.login(username, password)
        if user:
            SesionActual.iniciar(user)
            messagebox.showinfo("✅", f"¡Bienvenido, {username}!")
            self.root.withdraw()
            if user.rol == 'admin':
                AdminPanel(self.root, user)
            else:
                ClientePanel(self.root, user)
        else:
            messagebox.showerror("❌", "Usuario o contraseña incorrectos.")

    def toggle_mode(self):
        self.is_register = not self.is_register
        if self.is_register:
            self.root.title("📝 Registro - GymForTheMoment")
            self.create_register_fields()
        else:
            self.root.title("🔐 Iniciar Sesión - GymForTheMoment")
            self.main_frame.destroy()
            self.main_frame = ttk.Frame(self.root, padding=20)
            self.main_frame.pack(fill="both", expand=True)
            
            ttk.Label(self.main_frame, text="🏋️ GymForTheMoment", 
                      style='Header.TLabel').pack(pady=(0, 10))
            ttk.Label(self.main_frame, text="Tu gimnasio, disponible 24/7", 
                      style='Sub.TLabel').pack(pady=(0, 30))

            self.create_login_fields()

            btn_frame = ttk.Frame(self.main_frame)
            btn_frame.pack(pady=20)
            
            self.login_btn = ttk.Button(btn_frame, text="🔐 Iniciar Sesión", command=self.login)
            self.login_btn.pack(side="left", padx=5)
            
            self.toggle_btn = ttk.Button(btn_frame, text="✏️ Crear Cuenta", command=self.toggle_mode)
            self.toggle_btn.pack(side="left", padx=5)
            
            theme_btn = ttk.Button(self.main_frame, text="🌓 Cambiar tema", 
                                   command=lambda: toggle_theme(self.root), width=15)
            theme_btn.pack(pady=(10, 0))

    def register(self):
        name = self.entries["name_var"][0].get().strip()
        email = self.entries["email_var"][0].get().strip()
        phone = self.entries["phone_var"][0].get().strip()
        username = self.entries["username_var"][0].get().strip()
        password = self.entries["password_var"][0].get()

        if not all([name, email, phone, username, password]):
            messagebox.showwarning("⚠️", "Complete todos los campos.")
            return
        if not validar_email(email):
            messagebox.showerror("❌", "Email inválido.")
            return
        if not validar_usuario(username):
            messagebox.showerror("❌", "Usuario: 3-20 caracteres, solo letras/números.")
            return
        if len(password) < 4:
            messagebox.showerror("❌", "Contraseña mínima: 4 caracteres.")
            return

        try:
            cliente_data = {"nombre": name, "email": email, "telefono": phone}
            user = Usuario.create_cliente(username, password, cliente_data)
            messagebox.showinfo("✅", "¡Cuenta creada con éxito! Ahora inicia sesión.")
            
            self.is_register = False
            
            self.main_frame.destroy()
            self.main_frame = ttk.Frame(self.root, padding=20)
            self.main_frame.pack(fill="both", expand=True)
            self.setup_ui()
           
            self.username_var.set(username)
            self.password_var.set("")
            self.password_entry.focus_set() 
        except Exception as e:
            messagebox.showerror("❌", f"Error al registrar:\n{str(e)}")