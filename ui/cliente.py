# ui/cliente.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.aparato import Aparato
from models.clase import Clase
from models.sesion import Sesion
from models.recibo import Recibo
from utils import dia_a_nombre
from auth import SesionActual

class ClientePanel:
    def __init__(self, root, usuario):
        self.usuario = usuario
        self.window = tk.Toplevel(root)
        self.window.title(f"GymForTheMoment - Panel de {usuario.username}")
        self.window.geometry("1000x700")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Color scheme
        self.bg_color = "#f0f2f5"
        self.card_color = "#ffffff"
        self.header_color = "#2c3e50"
        self.accent_color = "#3498db"
        
        self.setup_ui()
    
    def setup_ui(self):
        # ============ HEADER ============
        header_frame = tk.Frame(self.window, bg=self.header_color, height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        # Título del gimnasio
        title_label = tk.Label(
            header_frame, 
            text="🏋️ Gym For The Moment", 
            font=("Segoe UI", 20, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Mensaje de bienvenida
        welcome_label = tk.Label(
            header_frame,
            text=f"👋 Bienvenido, {self.usuario.username}",
            font=("Segoe UI", 12),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        welcome_label.pack(side="left", padx=20)
        
        # Botón cerrar sesión
        logout_btn = tk.Button(
            header_frame,
            text="🚪 Cerrar Sesión",
            font=("Segoe UI", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.cerrar_sesion
        )
        logout_btn.pack(side="right", padx=20, pady=20)
        
        # ============ MAIN CONTENT ============
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Container para las 3 secciones
        sections_frame = tk.Frame(main_frame, bg=self.bg_color)
        sections_frame.pack(fill="both", expand=True)
        
        # Configurar grid con 3 columnas
        sections_frame.columnconfigure(0, weight=1)
        sections_frame.columnconfigure(1, weight=1)
        sections_frame.columnconfigure(2, weight=1)
        sections_frame.rowconfigure(0, weight=1)
        
        # ============ SECCIÓN 1: APARATOS ============
        self.create_aparatos_section(sections_frame)
        
        # ============ SECCIÓN 2: CLASES ============
        self.create_clases_section(sections_frame)
        
        # ============ SECCIÓN 3: PAGOS ============
        self.create_pagos_section(sections_frame)
    
    def create_aparatos_section(self, parent):
        """Sección de aparatos de gimnasio"""
        card = tk.Frame(parent, bg=self.card_color, relief="raised", bd=1)
        card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Título de la sección
        title_frame = tk.Frame(card, bg="#27ae60", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🏋️ Aparatos de Gimnasio",
            font=("Segoe UI", 14, "bold"),
            bg="#27ae60",
            fg="white"
        ).pack(pady=12)
        
        # Contenido
        content = tk.Frame(card, bg=self.card_color)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(
            content,
            text="Máquinas disponibles:",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_color,
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 5))
        
        # Lista de aparatos
        list_frame = tk.Frame(content, bg=self.card_color)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.aparatos_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            selectbackground="#3498db",
            selectforeground="white",
            relief="flat",
            yscrollcommand=scrollbar.set
        )
        self.aparatos_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.aparatos_listbox.yview)
        
        # Cargar aparatos
        aparatos = Aparato.listar()
        for ap in aparatos:
            self.aparatos_listbox.insert(tk.END, f"  {ap.nombre} ({ap.tipo})")
        
        # Botón
        tk.Button(
            content,
            text="📅 Reservar Aparato",
            font=("Segoe UI", 10, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.abrir_reserva_aparato
        ).pack(fill="x", pady=(10, 0))
        
        # Info adicional
        tk.Label(
            content,
            text="Reserva por 30 minutos",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#7f8c8d"
        ).pack(pady=(5, 0))
    
    def create_clases_section(self, parent):
        """Sección de clases grupales"""
        card = tk.Frame(parent, bg=self.card_color, relief="raised", bd=1)
        card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Título de la sección
        title_frame = tk.Frame(card, bg="#9b59b6", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🧘 Clases Grupales",
            font=("Segoe UI", 14, "bold"),
            bg="#9b59b6",
            fg="white"
        ).pack(pady=12)
        
        # Contenido
        content = tk.Frame(card, bg=self.card_color)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        tk.Label(
            content,
            text="Horarios disponibles:",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_color,
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 5))
        
        # Lista de clases con horarios
        list_frame = tk.Frame(content, bg=self.card_color)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.clases_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            selectbackground="#9b59b6",
            selectforeground="white",
            relief="flat",
            yscrollcommand=scrollbar.set
        )
        self.clases_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.clases_listbox.yview)
        
        # Cargar clases con horarios
        from models.clase_horario import ClaseHorario
        clases = Clase.listar()
        
        # Diccionario para mapear clase -> horarios
        self.clase_horarios_map = {}
        
        for c in clases:
            horarios = ClaseHorario.listar_por_clase(c.id)
            if horarios:
                # Agrupar horarios por día
                dias_dict = {}
                for h in horarios:
                    dia_nombre = dia_a_nombre(h.dia_semana)[:3]  # Lun, Mar, etc
                    if dia_nombre not in dias_dict:
                        dias_dict[dia_nombre] = []
                    dias_dict[dia_nombre].append(h.hora_inicio)
                
                # Formatear horarios
                horarios_str = ", ".join([f"{dia} {':'.join(horas)}" for dia, horas in dias_dict.items()])
                
                self.clases_listbox.insert(tk.END, f"  🏃 {c.nombre}")
                self.clases_listbox.insert(tk.END, f"     ⏰ {horarios_str}")
                self.clases_listbox.insert(tk.END, f"     👨‍🏫 {c.instructor} | ⏱ {c.duracion_min} min")
                self.clases_listbox.insert(tk.END, "")
                
                # Guardar mapeo para usar al reservar
                self.clase_horarios_map[c.id] = horarios
            else:
                # Clase sin horarios programados (mostrar info genérica)
                self.clases_listbox.insert(tk.END, f"  {c.nombre}")
                self.clases_listbox.insert(tk.END, f"     Instructor: {c.instructor}")
                self.clases_listbox.insert(tk.END, f"     Duración: {c.duracion_min} min")
                self.clases_listbox.insert(tk.END, "")
                self.clase_horarios_map[c.id] = []
        
        # Botón
        tk.Button(
            content,
            text="📝 Apuntarse a Clase",
            font=("Segoe UI", 10, "bold"),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.abrir_reserva_clase
        ).pack(fill="x", pady=(10, 0))
        
        # Info adicional
        tk.Label(
            content,
            text="Reserva tu plaza ahora",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#7f8c8d"
        ).pack(pady=(5, 0))
    
    def create_pagos_section(self, parent):
        """Sección de pagos y cuotas"""
        card = tk.Frame(parent, bg=self.card_color, relief="raised", bd=1)
        card.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Título de la sección
        title_frame = tk.Frame(card, bg="#e67e22", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="💳 Pagos y Cuotas",
            font=("Segoe UI", 14, "bold"),
            bg="#e67e22",
            fg="white"
        ).pack(pady=12)
        
        # Contenido
        content = tk.Frame(card, bg=self.card_color)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Resumen de cuotas
        recibos = Recibo.listar_por_cliente(self.usuario.id_cliente)
        pendientes = [r for r in recibos if not r['pagado']]
        pagados = [r for r in recibos if r['pagado']]
        
        # Info cuotas pendientes
        if pendientes:
            alert_frame = tk.Frame(content, bg="#ffe6e6", relief="solid", bd=1)
            alert_frame.pack(fill="x", pady=(0, 10))
            
            tk.Label(
                alert_frame,
                text=f"⚠️ {len(pendientes)} cuota(s) pendiente(s)",
                font=("Segoe UI", 10, "bold"),
                bg="#ffe6e6",
                fg="#c0392b"
            ).pack(pady=8)
        else:
            alert_frame = tk.Frame(content, bg="#e6ffe6", relief="solid", bd=1)
            alert_frame.pack(fill="x", pady=(0, 10))
            
            tk.Label(
                alert_frame,
                text="✅ ¡Al día con los pagos!",
                font=("Segoe UI", 10, "bold"),
                bg="#e6ffe6",
                fg="#27ae60"
            ).pack(pady=8)
        
        # Listado de recibos
        tk.Label(
            content,
            text="Historial de cuotas:",
            font=("Segoe UI", 10, "bold"),
            bg=self.card_color,
            fg="#2c3e50"
        ).pack(anchor="w", pady=(5, 5))
        
        list_frame = tk.Frame(content, bg=self.card_color)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.pagos_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            selectbackground="#e67e22",
            selectforeground="white",
            relief="flat",
            yscrollcommand=scrollbar.set
        )
        self.pagos_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.pagos_listbox.yview)
        
        # Cargar recibos
        for r in recibos:
            estado = "✅ Pagado" if r['pagado'] else "❌ Pendiente"
            self.pagos_listbox.insert(tk.END, f"  {r['mes']}/{r['anio']} - €{r['monto']:.2f}")
            self.pagos_listbox.insert(tk.END, f"     {estado}")
            self.pagos_listbox.insert(tk.END, "")
        
        # Botones
        btn_frame = tk.Frame(content, bg=self.card_color)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        tk.Button(
            btn_frame,
            text="💰 Pagar Cuota",
            font=("Segoe UI", 10, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.pagar_cuota
        ).pack(fill="x")
        
        # Info adicional
        tk.Label(
            content,
            text=f"Cuota mensual: €{Recibo.MONTO_MENSUAL:.2f}",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#7f8c8d"
        ).pack(pady=(5, 0))
    
    def abrir_reserva_aparato(self):
        """Abrir ventana de reserva de aparatos"""
        selection = self.aparatos_listbox.curselection()
        if not selection:
            messagebox.showwarning("⚠️", "Por favor, selecciona un aparato primero.")
            return
        
        idx = selection[0]
        aparatos = Aparato.listar()
        aparato = aparatos[idx]
        
        self.abrir_ventana_reserva(aparato, "aparato")
    
    def abrir_reserva_clase(self):
        """Abrir ventana de reserva de clases"""
        # Filtrar solo las líneas que contienen el nombre de la clase (no las de detalles)
        selection = self.clases_listbox.curselection()
        if not selection:
            messagebox.showwarning("⚠️", "Por favor, selecciona una clase primero.")
            return
        
        # Obtener la selección y encontrar la clase correspondiente
        idx = selection[0]
        clases = Clase.listar()
        
        # Cada clase ocupa 4 líneas en el listbox (nombre, instructor, duración, vacía)
        clase_idx = idx // 4
        if clase_idx >= len(clases):
            messagebox.showwarning("⚠️", "Por favor, selecciona una clase válida.")
            return
            
        clase = clases[clase_idx]
        self.abrir_ventana_reserva(clase, "clase")
    
    def abrir_ventana_reserva(self, item, tipo):
        """Ventana modal para reservar"""
        ventana = tk.Toplevel(self.window)
        ventana.title(f"Reservar {tipo.capitalize()}")
        ventana.geometry("400x350")
        ventana.resizable(False, False)
        ventana.grab_set()  # Modal
        
        # Header
        header = tk.Frame(ventana, bg="#3498db", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        nombre_item = item.nombre if hasattr(item, 'nombre') else str(item)
        tk.Label(
            header,
            text=f"📅 {nombre_item}",
            font=("Segoe UI", 14, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(pady=15)
        
        # Contenido
        content = tk.Frame(ventana, bg="white", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        # Si es clase, obtener horarios programados
        if tipo == "clase":
            from models.clase_horario import ClaseHorario
            horarios_programados = ClaseHorario.listar_por_clase(item.id)
            
            if not horarios_programados:
                tk.Label(
                    content,
                    text="⚠️ Esta clase no tiene horarios programados aún.",
                    font=("Segoe UI", 10),
                    bg="white",
                    fg="#e74c3c"
                ).pack(pady=50)
                
                tk.Button(
                    content,
                    text="Cerrar",
                    font=("Segoe UI", 10),
                    bg="#95a5a6",
                    fg="white",
                    relief="flat",
                    padx=20,
                    pady=10,
                    command=ventana.destroy
                ).pack()
                return
            
            # Agrupar por día/hora
            horarios_disponibles = {}
            for h in horarios_programados:
                dia = h.dia_semana
                hora = h.hora_inicio
                if dia not in horarios_disponibles:
                    horarios_disponibles[dia] = []
                horarios_disponibles[dia].append(hora)
        
        # Selector de día/hora
        tk.Label(
            content,
            text="Selecciona día y hora:",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 10))
        
        dia_var = tk.StringVar()
        hora_var = tk.StringVar()
        
        if tipo == "clase":
            # Mostrar solo días/horas programadas
            for dia in sorted(horarios_disponibles.keys()):
                dia_nombre = dia_a_nombre(dia)
                for hora in horarios_disponibles[dia]:
                    rb = ttk.Radiobutton(
                        content,
                        text=f"{dia_nombre} a las {hora}",
                        variable=dia_var,
                        value=f"{dia}|{hora}"
                    )
                    rb.pack(anchor="w", pady=2)
            
            if horarios_disponibles:
                primer_dia = sorted(horarios_disponibles.keys())[0]
                primera_hora = horarios_disponibles[primer_dia][0]
                dia_var.set(f"{primer_dia}|{primera_hora}")
        else:
            # Para aparatos, selector tradicional
            dia_frame = tk.Frame(content, bg="white")
            dia_frame.pack(fill="x", pady=(0, 15))
            
            dia_num_var = tk.StringVar(value="0")
            dias = [("Lun", "0"), ("Mar", "1"), ("Mié", "2"), ("Jue", "3"), ("Vie", "4")]
            for texto, val in dias:
                ttk.Radiobutton(
                    dia_frame,
                    text=texto,
                    variable=dia_num_var,
                    value=val,
                    command=lambda: actualizar_horas()
                ).pack(side="left", padx=5)
            
            tk.Label(
                content,
                text="Selecciona la hora:",
                font=("Segoe UI", 11, "bold"),
                bg="white"
            ).pack(anchor="w", pady=(0, 10))
            
            hora_combo = ttk.Combobox(
                content,
                textvariable=hora_var,
                state="readonly",
                width=15,
                font=("Segoe UI", 10)
            )
            hora_combo.pack(fill="x", pady=(0, 20))
            
            def actualizar_horas():
                dia = int(dia_num_var.get())
                ocupadas = Sesion.horas_ocupadas_por_aparato(item.id, dia)
                todas_franjas = [f"{h:02d}:{m:02d}" for h in range(6, 23) for m in (0, 30)]
                libres = [h for h in todas_franjas if h not in ocupadas]
                hora_combo['values'] = libres
                hora_combo.set(libres[0] if libres else "")
            
            actualizar_horas()
        
        # Botones
        btn_frame = tk.Frame(content, bg="white")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        def confirmar_reserva():
            if tipo == "clase":
                seleccion = dia_var.get()
                if not seleccion:
                    messagebox.showwarning("⚠️", "Selecciona un horario.")
                    return
                
                dia, hora = seleccion.split("|")
                dia = int(dia)
            else:
                hora = hora_var.get()
                dia = int(dia_num_var.get())
            
            if not hora:
                messagebox.showwarning("⚠️", "Selecciona una hora.")
                return
            
            try:
                if tipo == "aparato":
                    exito = Sesion.reservar(
                        self.usuario.id_cliente,
                        id_aparato=item.id,
                        dia_semana=dia,
                        hora_inicio=hora
                    )
                else:
                    exito = Sesion.reservar(
                        self.usuario.id_cliente,
                        id_clase=item.id,
                        dia_semana=dia,
                        hora_inicio=hora
                    )
                
                if exito:
                    messagebox.showinfo(
                        "✅",
                        f"¡Reserva confirmada!\\n{dia_a_nombre(dia)} a las {hora}"
                    )
                    ventana.destroy()
                else:
                    messagebox.showerror("❌", "Horario ya ocupado. Intenta con otro.")
            except Exception as e:
                messagebox.showerror("❌", f"Error: {e}")
        
        tk.Button(
            btn_frame,
            text="✅ Confirmar Reserva",
            font=("Segoe UI", 10, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=confirmar_reserva
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(
            btn_frame,
            text="❌ Cancelar",
            font=("Segoe UI", 10),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=ventana.destroy
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))
    
    def pagar_cuota(self):
        """Pagar cuota pendiente"""
        recibos = Recibo.listar_por_cliente(self.usuario.id_cliente)
        pendientes = [r for r in recibos if not r['pagado']]
        
        if not pendientes:
            messagebox.showinfo("ℹ️", "No tienes cuotas pendientes.")
            return
        
        # Ventana de selección
        ventana = tk.Toplevel(self.window)
        ventana.title("Pagar Cuota")
        ventana.geometry("400x400")
        ventana.resizable(False, False)
        ventana.grab_set()
        
        # Header
        header = tk.Frame(ventana, bg="#e67e22", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="💳 Pasarela de Pagos",
            font=("Segoe UI", 14, "bold"),
            bg="#e67e22",
            fg="white"
        ).pack(pady=15)
        
        # Contenido
        content = tk.Frame(ventana, bg="white", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Label(
            content,
            text="Selecciona la cuota a pagar:",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 10))
        
        # Lista de pendientes
        listbox = tk.Listbox(
            content,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            selectbackground="#e67e22"
        )
        listbox.pack(fill="both", expand=True, pady=(0, 15))
        
        for r in pendientes:
            listbox.insert(tk.END, f"{r['mes']}/{r['anio']} - €{r['monto']:.2f}")
        
        def confirmar_pago():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("⚠️", "Selecciona una cuota.")
                return
            
            recibo = pendientes[sel[0]]
            if messagebox.askyesno(
                "💡 Confirmar Pago",
                f"¿Confirmas el pago de €{recibo['monto']:.2f}\npara {recibo['mes']}/{recibo['anio']}?"
            ):
                Recibo.marcar_pagado(self.usuario.id_cliente, recibo['mes'], recibo['anio'])
                messagebox.showinfo("✅", "¡Pago procesado con éxito!")
                ventana.destroy()
                # Recargar ventana principal
                self.window.destroy()
                ClientePanel(self.window.master, self.usuario)
        
        tk.Button(
            content,
            text="💰 Pagar Ahora",
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            relief="flat",
            padx=20,
            pady=12,
            cursor="hand2",
            command=confirmar_pago
        ).pack(fill="x")
    
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("🚪 Cerrar Sesión", "¿Estás seguro que quieres cerrar sesión?"):
            SesionActual.cerrar()
            self.window.destroy()
            self.window.master.deiconify()
    
    def on_close(self):
        """Cerrar aplicación"""
        self.cerrar_sesion()