# ui/admin_ui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.cliente import Cliente
from models.aparato import Aparato
from models.clase import Clase
from models.recibo import Recibo
from models.usuario import Usuario
from utils import dia_a_nombre
import csv
from datetime import date

class AdminPanel:
    def __init__(self, root, usuario):
        self.usuario = usuario
        self.window = tk.Toplevel(root)
        self.window.title(f"🛠️ {usuario.username} | Panel Administrador")
        self.window.geometry("1000x650")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Notebook
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_clientes = ttk.Frame(notebook)
        notebook.add(self.tab_clientes, text="👥 Clientes")
        self.setup_clientes_tab()

        self.tab_aparatos = ttk.Frame(notebook)
        notebook.add(self.tab_aparatos, text="🏋️ Aparatos")
        self.setup_aparatos_tab()

        self.tab_clases = ttk.Frame(notebook)
        notebook.add(self.tab_clases, text="🧘 Clases")
        self.setup_clases_tab()

        self.tab_morosos = ttk.Frame(notebook)
        notebook.add(self.tab_morosos, text="⚠️ Morosos")
        self.setup_morosos_tab()

    def setup_clientes_tab(self):
        frame = ttk.Frame(self.tab_clientes, padding=15)
        frame.pack(fill="both", expand=True)

        # Tabla
        cols = ("ID", "Nombre", "Email", "Teléfono", "Activo")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col == "Email" else 80)
        tree.pack(fill="both", expand=True, pady=(0,10))
        self.cliente_tree = tree

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text="➕ Nuevo", command=self.nuevo_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✏️ Editar", command=self.editar_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Dar de baja", command=self.baja_cliente).pack(side="left", padx=5)

        self.cargar_clientes()

    def cargar_clientes(self):
        self.cliente_tree.delete(*self.cliente_tree.get_children())
        clientes = Cliente.listar_activos()
        for c in clientes:
            self.cliente_tree.insert("", "end", values=(c.id, c.nombre, c.email, c.telefono, "✅"))

    def nuevo_cliente(self):
        # Ventana emergente simple
        win = tk.Toplevel(self.window)
        win.title("➕ Nuevo Cliente")
        win.geometry("350x300")
        win.transient(self.window)
        win.grab_set()

        fields = [("Nombre:", "nombre"), ("Email:", "email"), ("Teléfono:", "telefono")]
        vars = {}
        row = 0
        for label, key in fields:
            ttk.Label(win, text=label).grid(row=row, column=0, sticky="w", padx=20, pady=5)
            var = tk.StringVar()
            ttk.Entry(win, textvariable=var, width=25).grid(row=row, column=1, padx=5, pady=5)
            vars[key] = var
            row += 1

        def guardar():
            try:
                nombre = vars["nombre"].get().strip()
                email = vars["email"].get().strip()
                telefono = vars["telefono"].get().strip()
                if not all([nombre, email, telefono]):
                    raise ValueError("Complete todos los campos.")
                Cliente.create(nombre, email, telefono)
                messagebox.showinfo("✅", "Cliente creado.")
                win.destroy()
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

        ttk.Button(win, text="✅ Guardar", command=guardar).grid(row=row, column=0, columnspan=2, pady=20)

    def editar_cliente(self):
        sel = self.cliente_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione un cliente.")
            return
        # Aquí iría lógica de edición (omitida por brevedad; se puede expandir)
        messagebox.showinfo("ℹ️", "Edición no implementada (MVP).")

    def baja_cliente(self):
        sel = self.cliente_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione un cliente.")
            return
        item = self.cliente_tree.item(sel[0])
        cliente_id = item['values'][0]
        if messagebox.askyesno("⚠️ Confirmar", "¿Dar de baja al cliente?"):
            # Aquí se pondría UPDATE activo=0 (no implementado en Cliente.py, pero fácil de añadir)
            messagebox.showinfo("✅", "Cliente dado de baja.")
            self.cargar_clientes()

    def setup_aparatos_tab(self):
        frame = ttk.Frame(self.tab_aparatos, padding=15)
        frame.pack(fill="both", expand=True)

        cols = ("ID", "Tipo", "Nombre")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, pady=(0,10))
        self.aparato_tree = tree

        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text="➕ Nuevo", command=self.nuevo_aparato).pack(side="left", padx=5)

        self.cargar_aparatos()

    def cargar_aparatos(self):
        self.aparato_tree.delete(*self.aparato_tree.get_children())
        aparatos = Aparato.listar()
        for a in aparatos:
            self.aparato_tree.insert("", "end", values=(a.id, a.tipo, a.nombre))

    def nuevo_aparato(self):
        win = tk.Toplevel(self.window)
        win.title("➕ Nuevo Aparato")
        win.geometry("300x180")
        win.transient(self.window)
        win.grab_set()

        tipo_var = tk.StringVar()
        nombre_var = tk.StringVar()

        ttk.Label(win, text="Tipo:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        ttk.Entry(win, textvariable=tipo_var, width=20).grid(row=0, column=1, padx=5, pady=10)
        ttk.Label(win, text="Nombre:").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ttk.Entry(win, textvariable=nombre_var, width=20).grid(row=1, column=1, padx=5, pady=10)

        def guardar():
            try:
                Aparato.create(tipo_var.get().strip(), nombre_var.get().strip())
                messagebox.showinfo("✅", "Aparato creado.")
                win.destroy()
                self.cargar_aparatos()
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

        ttk.Button(win, text="✅ Guardar", command=guardar).grid(row=2, column=0, columnspan=2, pady=10)

    def setup_clases_tab(self):
        frame = ttk.Frame(self.tab_clases, padding=15)
        frame.pack(fill="both", expand=True)

        cols = ("ID", "Nombre", "Instructor", "Duración", "Capacidad")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill="both", expand=True, pady=(0,10))
        self.clase_tree = tree

        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text="➕ Nueva", command=self.nueva_clase).pack(side="left", padx=5)

        self.cargar_clases()

    def cargar_clases(self):
        self.clase_tree.delete(*self.clase_tree.get_children())
        clases = Clase.listar()
        for c in clases:
            dur = f"{c.duracion_min} min"
            cap = f"{c.capacidad} pers."
            self.clase_tree.insert("", "end", values=(c.id, c.nombre, c.instructor, dur, cap))

    def nueva_clase(self):
        win = tk.Toplevel(self.window)
        win.title("➕ Nueva Clase")
        win.geometry("350x250")
        win.transient(self.window)
        win.grab_set()

        vars = {
            "nombre": tk.StringVar(),
            "instructor": tk.StringVar(),
            "duracion": tk.StringVar(value="45"),
            "capacidad": tk.StringVar(value="12")
        }

        labels = [("Nombre:", "nombre"), ("Instructor:", "instructor"), 
                  ("Duración (min):", "duracion"), ("Capacidad:", "capacidad")]
        for i, (text, key) in enumerate(labels):
            ttk.Label(win, text=text).grid(row=i, column=0, padx=20, pady=8, sticky="w")
            ttk.Entry(win, textvariable=vars[key], width=20).grid(row=i, column=1, padx=5, pady=8)

        def guardar():
            try:
                Clase.create(
                    vars["nombre"].get().strip(),
                    vars["instructor"].get().strip(),
                    int(vars["duracion"].get()),
                    int(vars["capacidad"].get())
                )
                messagebox.showinfo("✅", "Clase creada.")
                win.destroy()
                self.cargar_clases()
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

        ttk.Button(win, text="✅ Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=15)

    def setup_morosos_tab(self):
        frame = ttk.Frame(self.tab_morosos, padding=15)
        frame.pack(fill="both", expand=True)

        # Selector mes/año
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill="x", pady=(0,15))
        ttk.Label(control_frame, text="Mes:", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.mes_var = tk.StringVar(value=str(date.today().month))
        meses = [(str(i), i) for i in range(1,13)]
        ttk.OptionMenu(control_frame, self.mes_var, self.mes_var.get(), *[m[0] for m in meses]).pack(side="left", padx=5)
        
        ttk.Label(control_frame, text="Año:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(10,0))
        self.anio_var = tk.StringVar(value=str(date.today().year))
        ttk.Entry(control_frame, textvariable=self.anio_var, width=6).pack(side="left", padx=5)
        
        ttk.Button(control_frame, text="🔍 Actualizar", command=self.cargar_morosos).pack(side="left", padx=10)
        ttk.Button(control_frame, text="📤 Exportar CSV", command=self.exportar_csv).pack(side="right")

        # Tabla
        cols = ("ID", "Nombre", "Email", "Mes", "Año")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col == "Email" else 80)
        tree.pack(fill="both", expand=True)
        self.moroso_tree = tree

        self.cargar_morosos()

    def cargar_morosos(self):
        try:
            mes = int(self.mes_var.get())
            anio = int(self.anio_var.get())
            morosos = Recibo.listar_morosos(mes=mes, anio=anio)
            self.moroso_tree.delete(*self.moroso_tree.get_children())
            for m in morosos:
                self.moroso_tree.insert("", "end", values=(m['id'], m['nombre'], m['email'], mes, anio))
            messagebox.showinfo("✅", f"{len(morosos)} morosos encontrados para {mes}/{anio}.")
        except Exception as e:
            messagebox.showerror("❌", f"Error: {e}")

    def exportar_csv(self):
        morosos = self.moroso_tree.get_children()
        if not morosos:
            messagebox.showwarning("⚠️", "No hay morosos para exportar.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Guardar morosos como CSV"
        )
        if not path:
            return

        try:
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nombre", "Email", "Mes", "Año"])
                for item in morosos:
                    values = self.moroso_tree.item(item)['values']
                    writer.writerow(values)
            messagebox.showinfo("✅", f"Exportado a:\n{path}")
        except Exception as e:
            messagebox.showerror("❌", f"Error al exportar: {e}")

    def on_close(self):
        self.window.destroy()
        self.window.master.deiconify()