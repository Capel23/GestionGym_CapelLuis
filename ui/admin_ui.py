import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.cliente import Cliente
from models.aparato import Aparato
from models.clase import Clase
from models.recibo import Recibo
from models.sesion import Sesion
from models.usuario import Usuario
from utils import dia_a_nombre, set_window_icon
import csv
from datetime import date

class AdminPanel:
    def __init__(self, root, usuario):
        self.usuario = usuario
        self.window = tk.Toplevel(root)
        self.window.title(f"🛠️ {usuario.username} | Panel Administrador")
        self.window.geometry("1200x700")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        
        set_window_icon(self.window)


        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

    
        self.tab_clientes = ttk.Frame(notebook)
        notebook.add(self.tab_clientes, text="👥 Clientes")
        self.setup_clientes_tab()

     
        self.tab_reservas = ttk.Frame(notebook)
        notebook.add(self.tab_reservas, text="📅 Reservas")
        self.setup_reservas_tab()

     
        self.tab_aparatos = ttk.Frame(notebook)
        notebook.add(self.tab_aparatos, text="🏋️ Aparatos")
        self.setup_aparatos_tab()

        self.tab_clases = ttk.Frame(notebook)
        notebook.add(self.tab_clases, text="🧘 Clases")
        self.setup_clases_tab()

       
        self.tab_pagos = ttk.Frame(notebook)
        notebook.add(self.tab_pagos, text="💰 Pagos y Recibos")
        self.setup_pagos_tab()


    def setup_clientes_tab(self):
        frame = ttk.Frame(self.tab_clientes, padding=15)
        frame.pack(fill="both", expand=True)

        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(search_frame, text="🔍 Buscar:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.cliente_search_var = tk.StringVar()
        self.cliente_search_var.trace('w', lambda *args: self.buscar_clientes())
        ttk.Entry(search_frame, textvariable=self.cliente_search_var, width=30).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Limpiar", command=self.limpiar_busqueda_clientes).pack(side="left", padx=5)

        cols = ("ID", "Nombre", "Email", "Teléfono", "Activo", "Reservas", "Estado Pago")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            if col == "Email":
                tree.column(col, width=150)
            elif col in ["Reservas", "Activo", "ID"]:
                tree.column(col, width=70)
            elif col == "Estado Pago":
                tree.column(col, width=100)
            else:
                tree.column(col, width=120)
        tree.pack(fill="both", expand=True, pady=(0,10))
        self.cliente_tree = tree

        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text="➕ Nuevo", command=self.nuevo_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✏️ Editar", command=self.editar_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Dar de baja", command=self.baja_cliente).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_clientes).pack(side="left", padx=5)

        self.cargar_clientes()

    def cargar_clientes(self):
        self.cliente_tree.delete(*self.cliente_tree.get_children())
        clientes = Cliente.listar_activos()
        for c in clientes:
           
            num_reservas = Sesion.contar_por_cliente(c.id)
            ultimo_pago = Recibo.get_ultimo_pago(c.id)
            estado_pago = "✅ Al día" if ultimo_pago else "⚠️ Sin pagos"
            
            self.cliente_tree.insert("", "end", values=(
                c.id, c.nombre, c.email, c.telefono, "✅", 
                num_reservas, estado_pago
            ))

    def buscar_clientes(self):
        termino = self.cliente_search_var.get().strip()
        self.cliente_tree.delete(*self.cliente_tree.get_children())
        
        if not termino:
            self.cargar_clientes()
            return
        
        clientes = Cliente.buscar(termino)
        for c in clientes:
            num_reservas = Sesion.contar_por_cliente(c.id)
            ultimo_pago = Recibo.get_ultimo_pago(c.id)
            estado_pago = "✅ Al día" if ultimo_pago else "⚠️ Sin pagos"
            
            self.cliente_tree.insert("", "end", values=(
                c.id, c.nombre, c.email, c.telefono, "✅", 
                num_reservas, estado_pago
            ))

    def limpiar_busqueda_clientes(self):
        self.cliente_search_var.set("")
        self.cargar_clientes()

    def nuevo_cliente(self):
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
        
        item = self.cliente_tree.item(sel[0])
        cliente_id = item['values'][0]
        cliente = Cliente.get_by_id(cliente_id)
        
        if not cliente:
            messagebox.showerror("❌", "Cliente no encontrado.")
            return

        win = tk.Toplevel(self.window)
        win.title("✏️ Editar Cliente")
        win.geometry("350x300")
        win.transient(self.window)
        win.grab_set()

       
        fields = [
            ("Nombre:", "nombre", cliente.nombre),
            ("Email:", "email", cliente.email),
            ("Teléfono:", "telefono", cliente.telefono)
        ]
        vars = {}
        row = 0
        for label, key, valor_actual in fields:
            ttk.Label(win, text=label).grid(row=row, column=0, sticky="w", padx=20, pady=5)
            var = tk.StringVar(value=valor_actual)
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
                
                Cliente.update(cliente_id, nombre=nombre, email=email, telefono=telefono)
                messagebox.showinfo("✅", "Cliente actualizado correctamente.")
                win.destroy()
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

        ttk.Button(win, text="✅ Guardar Cambios", command=guardar).grid(row=row, column=0, columnspan=2, pady=20)

    def baja_cliente(self):
        sel = self.cliente_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione un cliente.")
            return
        item = self.cliente_tree.item(sel[0])
        cliente_id = item['values'][0]
        cliente_nombre = item['values'][1]
        
        if messagebox.askyesno("⚠️ Confirmar", f"¿Dar de baja a '{cliente_nombre}'?\n\nEsto marcará al cliente como inactivo."):
            try:
                Cliente.dar_de_baja(cliente_id)
                messagebox.showinfo("✅", "Cliente dado de baja correctamente.")
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

    def setup_reservas_tab(self):
        frame = ttk.Frame(self.tab_reservas, padding=15)
        frame.pack(fill="both", expand=True)

        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(filter_frame, text="Filtros:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)

        ttk.Label(filter_frame, text="Tipo:").pack(side="left", padx=5)
        self.reserva_tipo_var = tk.StringVar(value="todos")
        tipos = [("Todos", "todos"), ("Aparatos", "aparato"), ("Clases", "clase")]
        for texto, val in tipos:
            ttk.Radiobutton(
                filter_frame,
                text=texto,
                variable=self.reserva_tipo_var,
                value=val,
                command=self.cargar_reservas
            ).pack(side="left", padx=2)

     
        ttk.Label(filter_frame, text="Día:").pack(side="left", padx=(15, 5))
        self.reserva_dia_var = tk.StringVar(value="todos")
        dias = [("Todos", "todos"), ("Lun", "0"), ("Mar", "1"), ("Mié", "2"), ("Jue", "3"), ("Vie", "4")]
        for texto, val in dias:
            ttk.Radiobutton(
                filter_frame,
                text=texto,
                variable=self.reserva_dia_var,
                value=val,
                command=self.cargar_reservas
            ).pack(side="left", padx=2)

       
        cols = ("ID", "Cliente", "Tipo", "Recurso", "Día", "Hora", "Fecha Reserva")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            if col == "ID":
                tree.column(col, width=50)
            elif col == "Recurso":
                tree.column(col, width=150)
            elif col in ["Tipo", "Día", "Hora"]:
                tree.column(col, width=80)
            else:
                tree.column(col, width=120)
        tree.pack(fill="both", expand=True, pady=(0, 10))
        self.reserva_tree = tree

       
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text="❌ Cancelar Reserva", command=self.cancelar_reserva).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_reservas).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📄 Ver Detalles", command=self.ver_detalles_reserva).pack(side="left", padx=5)

        self.cargar_reservas()

    def cargar_reservas(self):
        self.reserva_tree.delete(*self.reserva_tree.get_children())

    
        tipo = self.reserva_tipo_var.get()
        dia = self.reserva_dia_var.get()

        filtro_tipo = None if tipo == "todos" else tipo
        filtro_dia = None if dia == "todos" else int(dia)

        reservas = Sesion.listar_todas(filtro_tipo=filtro_tipo, filtro_dia=filtro_dia)

        for r in reservas:
            tipo_str = "Aparato" if r['id_aparato'] else "Clase"
            recurso = r['aparato_nombre'] if r['id_aparato'] else r['clase_nombre']
            dia_nombre = dia_a_nombre(r['dia_semana'])
            
            self.reserva_tree.insert("", "end", values=(
                r['id'],
                r['cliente_nombre'],
                tipo_str,
                recurso,
                dia_nombre,
                r['hora_inicio'],
                r['fecha_reserva']
            ))

    def cancelar_reserva(self):
        sel = self.reserva_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione una reserva.")
            return

        item = self.reserva_tree.item(sel[0])
        reserva_id = item['values'][0]
        cliente = item['values'][1]
        recurso = item['values'][3]

        if messagebox.askyesno("⚠️ Confirmar", f"¿Cancelar la reserva de {cliente} para '{recurso}'?"):
            try:
                if Sesion.cancelar(reserva_id):
                    messagebox.showinfo("✅", "Reserva cancelada correctamente.")
                    self.cargar_reservas()
                else:
                    messagebox.showerror("❌", "No se pudo cancelar la reserva.")
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

    def ver_detalles_reserva(self):
        sel = self.reserva_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione una reserva.")
            return

        item = self.reserva_tree.item(sel[0])
        reserva_id = item['values'][0]
        reserva = Sesion.get_by_id(reserva_id)

        if not reserva:
            messagebox.showerror("❌", "Reserva no encontrada.")
            return

     
        win = tk.Toplevel(self.window)
        win.title("📄 Detalles de Reserva")
        win.geometry("400x350")
        win.transient(self.window)
        win.grab_set()

        info_frame = ttk.Frame(win, padding=20)
        info_frame.pack(fill="both", expand=True)

        tipo = "Aparato" if reserva['id_aparato'] else "Clase"
        recurso = reserva['aparato_nombre'] if reserva['id_aparato'] else reserva['clase_nombre']

        detalles = [
            ("ID Reserva:", reserva['id']),
            ("Cliente:", reserva['cliente_nombre']),
            ("Tipo:", tipo),
            ("Recurso:", recurso),
            ("Día:", dia_a_nombre(reserva['dia_semana'])),
            ("Hora:", reserva['hora_inicio']),
            ("Fecha de Reserva:", reserva['fecha_reserva'])
        ]

        for i, (label, valor) in enumerate(detalles):
            ttk.Label(info_frame, text=label, font=("Segoe UI", 9, "bold")).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Label(info_frame, text=str(valor), font=("Segoe UI", 9)).grid(row=i, column=1, sticky="w", padx=10, pady=5)

        ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=10)

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
        ttk.Button(btn_frame, text="✏️ Editar", command=self.editar_aparato).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Eliminar", command=self.eliminar_aparato).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_aparatos).pack(side="left", padx=5)

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
    
    def editar_aparato(self):
        sel = self.aparato_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione un aparato.")
            return
        
        item = self.aparato_tree.item(sel[0])
        aparato_id = item['values'][0]
        aparato = Aparato.get_by_id(aparato_id)
        
        if not aparato:
            messagebox.showerror("❌", "Aparato no encontrado.")
            return

        win = tk.Toplevel(self.window)
        win.title("✏️ Editar Aparato")
        win.geometry("300x180")
        win.transient(self.window)
        win.grab_set()

        tipo_var = tk.StringVar(value=aparato.tipo)
        nombre_var = tk.StringVar(value=aparato.nombre)

        ttk.Label(win, text="Tipo:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        ttk.Entry(win, textvariable=tipo_var, width=20).grid(row=0, column=1, padx=5, pady=10)
        ttk.Label(win, text="Nombre:").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ttk.Entry(win, textvariable=nombre_var, width=20).grid(row=1, column=1, padx=5, pady=10)

        def guardar():
            try:
                tipo = tipo_var.get().strip()
                nombre = nombre_var.get().strip()
                if not tipo or not nombre:
                    raise ValueError("Complete todos los campos.")
                
                if Aparato.update(aparato_id, tipo, nombre):
                    messagebox.showinfo("✅", "Aparato actualizado correctamente.")
                    win.destroy()
                    self.cargar_aparatos()
                else:
                    messagebox.showerror("❌", "Error al actualizar el aparato.")
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

        ttk.Button(win, text="✅ Guardar Cambios", command=guardar).grid(row=2, column=0, columnspan=2, pady=10)
    
    def eliminar_aparato(self):
        sel = self.aparato_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione un aparato.")
            return
        
        item = self.aparato_tree.item(sel[0])
        aparato_id = item['values'][0]
        aparato_nombre = item['values'][2]
        
        if Aparato.tiene_reservas(aparato_id):
            messagebox.showwarning(
                "⚠️ No se puede eliminar",
                f"El aparato '{aparato_nombre}' tiene reservas activas.\n\n"
                "Cancele primero las reservas antes de eliminar."
            )
            return
        
        if messagebox.askyesno("⚠️ Confirmar", f"¿eliminar el aparato '{aparato_nombre}'?\n\nEsta acción no se puede deshacer."):
            try:
                if Aparato.delete(aparato_id):
                    messagebox.showinfo("✅", "Aparato eliminado correctamente.")
                    self.cargar_aparatos()
                else:
                    messagebox.showerror("❌", "Error al eliminar el aparato.")
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

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
        ttk.Button(btn_frame, text="✏️ Editar", command=self.editar_clase).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Eliminar", command=self.eliminar_clase).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📅 Gestionar Horarios", command=self.gestionar_horarios_clase).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_clases).pack(side="left", padx=5)

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
    
    def editar_clase(self):
        sel = self.clase_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione una clase.")
            return
        
        item = self.clase_tree.item(sel[0])
        clase_id = item['values'][0]
        clase = Clase.get_by_id(clase_id)
        
        if not clase:
            messagebox.showerror("❌", "Clase no encontrada.")
            return

        win = tk.Toplevel(self.window)
        win.title("✏️ Editar Clase")
        win.geometry("350x250")
        win.transient(self.window)
        win.grab_set()

        vars = {
            "nombre": tk.StringVar(value=clase.nombre),
            "instructor": tk.StringVar(value=clase.instructor),
            "duracion": tk.StringVar(value=str(clase.duracion_min)),
            "capacidad": tk.StringVar(value=str(clase.capacidad))
        }

        labels = [("Nombre:", "nombre"), ("Instructor:", "instructor"), 
                  ("Duración (min):", "duracion"), ("Capacidad:", "capacidad")]
        for i, (text, key) in enumerate(labels):
            ttk.Label(win, text=text).grid(row=i, column=0, padx=20, pady=8, sticky="w")
            ttk.Entry(win, textvariable=vars[key], width=20).grid(row=i, column=1, padx=5, pady=8)

        def guardar():
            try:
                nombre = vars["nombre"].get().strip()
                instructor = vars["instructor"].get().strip()
                duracion = int(vars["duracion"].get())
                capacidad = int(vars["capacidad"].get())
                
                if not nombre or not instructor:
                    raise ValueError("Complete todos los campos.")
                
                if Clase.update(clase_id, nombre, instructor, duracion, capacidad):
                    messagebox.showinfo("✅", "Clase actualizada correctamente.")
                    win.destroy()
                    self.cargar_clases()
                else:
                    messagebox.showerror("❌", "Error al actualizar la clase.")
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

        ttk.Button(win, text="✅ Guardar Cambios", command=guardar).grid(row=4, column=0, columnspan=2, pady=15)
    
    def eliminar_clase(self):
        sel =self.clase_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione una clase.")
            return
        
        item = self.clase_tree.item(sel[0])
        clase_id = item['values'][0]
        clase_nombre = item['values'][1]
        
        if Clase.tiene_reservas(clase_id):
            messagebox.showwarning(
                "⚠️ No se puede eliminar",
                f"La clase '{clase_nombre}' tiene reservas activas.\n\n"
                "Cancele primero las reservas antes de eliminar."
            )
            return
        
        if messagebox.askyesno("⚠️ Confirmar", f"¿eliminar la clase '{clase_nombre}'?\n\nEsta acción también eliminará todos sus horarios."):
            try:
                if Clase.delete(clase_id):
                    messagebox.showinfo("✅", "Clase eliminada correctamente.")
                    self.cargar_clases()
                else:
                    messagebox.showerror("❌", "Error al eliminar la clase.")
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")
    
    def gestionar_horarios_clase(self):
        sel = self.clase_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione una clase.")
            return
        
        item = self.clase_tree.item(sel[0])
        clase_id = item['values'][0]
        clase_nombre = item['values'][1]
        
        ventana = tk.Toplevel(self.window)
        ventana.title(f"📅 Horarios de '{clase_nombre}'")
        ventana.geometry("500x450")
        ventana.transient(self.window)
        ventana.grab_set()
        
        header = tk.Frame(ventana, bg="#9b59b6", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"📅 Horarios de {clase_nombre}",
            font=("Segoe UI", 12, "bold"),
            bg="#9b59b6",
            fg="white"
        ).pack(pady=12)
        
        content = tk.Frame(ventana, padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        cols = ("ID", "Día", "Hora")
        tree = ttk.Treeview(content, columns=cols, show="headings", height=12)
        for col in cols:
            tree.heading(col, text=col)
            if col == "ID":
                tree.column(col, width=50)
            else:
                tree.column(col, width=150)
        tree.pack(fill="both", expand=True, pady=(0, 10))
        
        from models.clase_horario import ClaseHorario
        
        def cargar_horarios():
            tree.delete(*tree.get_children())
            horarios = ClaseHorario.listar_por_clase(clase_id)
            for h in horarios:
                dia_nombre = dia_a_nombre(h.dia_semana)
                tree.insert("", "end", values=(h.id, dia_nombre, h.hora_inicio))
        
        def nuevo_horario():
            win_horario = tk.Toplevel(ventana)
            win_horario.title("➕ Nuevo Horario")
            win_horario.geometry("300x200")
            win_horario.transient(ventana)
            win_horario.grab_set()
            
            ttk.Label(win_horario, text="Día de la semana:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
            dia_var = tk.StringVar(value="0")
            dias = [("Lunes", "0"), ("Martes", "1"), ("Miércoles", "2"), ("Jueves", "3"), ("Viernes", "4")]
            dia_combo = ttk.Combobox(win_horario, textvariable=dia_var, values=[d[1] for d in dias], state="readonly", width=18)
            dia_combo.grid(row=0, column=1, padx=5, pady=10)
            dia_combo.set("0")
            
            ttk.Label(win_horario, text="Hora (HH:MM):").grid(row=1, column=0, padx=20, pady=10, sticky="w")
            hora_var = tk.StringVar(value="18:00")
            ttk.Entry(win_horario, textvariable=hora_var, width=20).grid(row=1, column=1, padx=5, pady=10)
            
            def guardar_horario():
                try:
                    dia = int(dia_var.get())
                    hora = hora_var.get().strip()
                    
                    if ClaseHorario.existe_horario(clase_id, dia, hora):
                        messagebox.showwarning("⚠️", "Ya existe un horario para este día y hora.")
                        return
                    
                    ClaseHorario.create(clase_id, dia, hora)
                    messagebox.showinfo("✅", "Horario creado correctamente.")
                    win_horario.destroy()
                    cargar_horarios()
                except Exception as e:
                    messagebox.showerror("❌", f"Error: {e}")
            
            ttk.Button(win_horario, text="✅ Guardar", command=guardar_horario).grid(row=2, column=0, columnspan=2, pady=15)
        
        def eliminar_horario():
            sel_horario = tree.selection()
            if not sel_horario:
                messagebox.showwarning("⚠️", "Seleccione un horario.")
                return
            
            item_horario = tree.item(sel_horario[0])
            horario_id = item_horario['values'][0]
            
            if messagebox.askyesno("⚠️ Confirmar", "¿eliminar este horario?"):
                try:
                    if ClaseHorario.delete(horario_id):
                        messagebox.showinfo("✅", "Horario eliminado correctamente.")
                        cargar_horarios()
                    else:
                        messagebox.showerror("❌", "Error al eliminar el horario.")
                except Exception as e:
                    messagebox.showerror("❌", f"Error: {e}")
        
        cargar_horarios()
        
        btn_frame = tk.Frame(content)
        btn_frame.pack(fill="x", pady=(0, 0))
        ttk.Button(btn_frame, text="➕ Nuevo Horario", command=nuevo_horario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Eliminar Horario", command=eliminar_horario).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cerrar", command=ventana.destroy).pack(side="right", padx=5)

    def setup_pagos_tab(self):
        frame = ttk.Frame(self.tab_pagos, padding=15)
        frame.pack(fill="both", expand=True)

       
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill="x", pady=(0,15))

     
        ttk.Label(control_frame, text="Estado:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.pago_estado_var = tk.StringVar(value="todos")
        estados = [("Todos", "todos"), ("Pendientes", "pendiente"), ("Pagados", "pagado")]
        for texto, val in estados:
            ttk.Radiobutton(
                control_frame,
                text=texto,
                variable=self.pago_estado_var,
                value=val,
                command=self.cargar_pagos
            ).pack(side="left", padx=2)

        
        ttk.Label(control_frame, text="Mes:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(15, 5))
        self.pago_mes_var = tk.StringVar(value="todos")
        meses_opciones = ["todos"] + [str(i) for i in range(1, 13)]
        ttk.OptionMenu(control_frame, self.pago_mes_var, self.pago_mes_var.get(), *meses_opciones, command=lambda _: self.cargar_pagos()).pack(side="left", padx=5)
        
        ttk.Label(control_frame, text="Año:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.pago_anio_var = tk.StringVar(value="todos")
        ttk.Entry(control_frame, textvariable=self.pago_anio_var, width=8).pack(side="left", padx=5)
        
        ttk.Button(control_frame, text="🔍 Filtrar", command=self.cargar_pagos).pack(side="left", padx=10)

        
        action_frame = ttk.Frame(frame)
        action_frame.pack(fill="x", pady=(0, 10))
        ttk.Button(action_frame, text="💰 Marcar como Pagado", command=self.marcar_como_pagado).pack(side="left", padx=5)
        ttk.Button(action_frame, text="➕ Generar Recibos del Mes", command=self.generar_recibos_mes).pack(side="left", padx=5)
        ttk.Button(action_frame, text="📤 Exportar CSV", command=self.exportar_pagos_csv).pack(side="right", padx=5)

       
        cols = ("ID", "Cliente", "Email", "Mes", "Año", "Monto", "Estado", "Fecha Pago")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for col in cols:
            tree.heading(col, text=col)
            if col == "Email":
                tree.column(col, width=150)
            elif col in ["ID", "Mes", "Año"]:
                tree.column(col, width=50)
            elif col == "Monto":
                tree.column(col, width=70)
            else:
                tree.column(col, width=100)
        tree.pack(fill="both", expand=True)
        self.pago_tree = tree

        self.cargar_pagos()

    def cargar_pagos(self):
        self.pago_tree.delete(*self.pago_tree.get_children())

      
        estado = self.pago_estado_var.get()
        mes = self.pago_mes_var.get()
        anio = self.pago_anio_var.get()

        filtro_estado = None if estado == "todos" else estado
        filtro_mes = None if mes == "todos" else int(mes)
        filtro_anio = None if anio == "todos" or not anio.strip() else int(anio)

        recibos = Recibo.listar_todos(
            filtro_estado=filtro_estado,
            filtro_mes=filtro_mes,
            filtro_anio=filtro_anio
        )

        for r in recibos:
            estado_str = "✅ Pagado" if r['pagado'] else "❌ Pendiente"
            fecha_pago = r['fecha_pago'] if r['fecha_pago'] else "-"
            
            self.pago_tree.insert("", "end", values=(
                r['id'],
                r['cliente_nombre'],
                r['cliente_email'],
                r['mes'],
                r['anio'],
                f"€{r['monto']:.2f}",
                estado_str,
                fecha_pago
            ))

    def marcar_como_pagado(self):
        sel = self.pago_tree.selection()
        if not sel:
            messagebox.showwarning("⚠️", "Seleccione un recibo.")
            return

        item = self.pago_tree.item(sel[0])
        recibo_id = item['values'][0]
        cliente_nombre = item['values'][1]
        mes = item['values'][3]
        anio = item['values'][4]
        estado = item['values'][6]

        if "Pagado" in estado:
            messagebox.showinfo("ℹ️", "Este recibo ya está marcado como pagado.")
            return

        if messagebox.askyesno("💰 Confirmar", f"¿Marcar como pagado el recibo de {cliente_nombre} ({mes}/{anio})?"):
           
            from database import get_db_connection
            conn = get_db_connection()
            id_cliente = conn.execute("SELECT id_cliente FROM recibo WHERE id = ?", (recibo_id,)).fetchone()['id_cliente']
            conn.close()

            if Recibo.marcar_pagado(id_cliente, mes, anio):
                messagebox.showinfo("✅", "Recibo marcado como pagado.")
                self.cargar_pagos()
            else:
                messagebox.showerror("❌", "No se pudo marcar el recibo como pagado.")

    def generar_recibos_mes(self):
        hoy = date.today()
        if messagebox.askyesno("➕ Generar Recibos", f"¿Generar recibos para todos los clientes activos del mes {hoy.month}/{hoy.year}?"):
            try:
                creados = Recibo.generar_recibos_mes()
                messagebox.showinfo("✅", f"Se generaron {creados} nuevo(s) recibo(s).")
                self.cargar_pagos()
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")

    def exportar_pagos_csv(self):
        recibos = self.pago_tree.get_children()
        if not recibos:
            messagebox.showwarning("⚠️", "No hay recibos para exportar.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Guardar recibos como CSV"
        )
        if not path:
            return

        try:
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Cliente", "Email", "Mes", "Año", "Monto", "Estado", "Fecha Pago"])
                for item in recibos:
                    values = self.pago_tree.item(item)['values']
                    writer.writerow(values)
            messagebox.showinfo("✅", f"Exportado a:\n{path}")
        except Exception as e:
            messagebox.showerror("❌", f"Error al exportar: {e}")

    def on_close(self):
        self.window.destroy()
        self.window.master.deiconify()