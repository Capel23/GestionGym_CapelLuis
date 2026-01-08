import tkinter as tk
from tkinter import ttk, messagebox
from models.aparato import Aparato
from models.clase import Clase
from models.sesion import Sesion
from models.recibo import Recibo
from utils import dia_a_nombre, set_window_icon
from auth import SesionActual
from database import get_db_connection

class ClientePanel:
    def __init__(self, root, usuario):
        self.usuario = usuario
        self.window = tk.Toplevel(root)
        self.window.title(f"GymForTheMoment - Panel de {usuario.username}")
        self.window.geometry("1500x700")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
       
        set_window_icon(self.window)
        
       
        self.bg_color = "#f0f2f5"
        self.card_color = "#ffffff"
        self.header_color = "#2c3e50"
        self.accent_color = "#3498db"
        
        self.setup_ui()
    
    def setup_ui(self):
      
        header_frame = tk.Frame(self.window, bg=self.header_color, height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
       
        title_label = tk.Label(
            header_frame, 
            text="🏋️ Gym For The Moment", 
            font=("Segoe UI", 20, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title_label.pack(side="left", padx=20, pady=20)
        
     
        welcome_label = tk.Label(
            header_frame,
            text=f"👋 Bienvenido, {self.usuario.username}",
            font=("Segoe UI", 12),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        welcome_label.pack(side="left", padx=20)
        
      
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
        
       
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
       
        sections_frame = tk.Frame(main_frame, bg=self.bg_color)
        sections_frame.pack(fill="both", expand=True)
        
       
        sections_frame.columnconfigure(0, weight=1)
        sections_frame.columnconfigure(1, weight=1)
        sections_frame.columnconfigure(2, weight=1)
        sections_frame.rowconfigure(0, weight=1)
        
       
        self.create_aparatos_section(sections_frame)
        
      
        self.create_clases_section(sections_frame)
        
      
        self.create_pagos_section(sections_frame)
    
    def create_aparatos_section(self, parent):
        """Sección de aparatos de gimnasio con visualización mejorada"""
        card = tk.Frame(parent, bg=self.card_color, relief="raised", bd=1)
        card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
       
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
        
       
        content_wrapper = tk.Frame(card, bg=self.card_color)
        content_wrapper.pack(fill="both", expand=True, padx=10, pady=10)
        
        
        canvas = tk.Canvas(content_wrapper, bg=self.card_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_wrapper, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.card_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
       
        filter_frame = tk.Frame(scrollable_frame, bg=self.card_color)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            filter_frame,
            text="📋 Selecciona día para ver disponibilidad:",
            font=("Segoe UI", 9, "bold"),
            bg=self.card_color,
            fg="#2c3e50"
        ).pack(side="left", padx=5)
        
        self.dia_var = tk.StringVar(value="0")
        dias = [("Lun", "0"), ("Mar", "1"), ("Mié", "2"), ("Jue", "3"), ("Vie", "4")]
        
        for texto, val in dias:
            btn = tk.Radiobutton(
                filter_frame,
                text=texto,
                variable=self.dia_var,
                value=val,
                font=("Segoe UI", 8),
                bg=self.card_color,
                activebackground=self.card_color,
                selectcolor="#27ae60",
                command=self.actualizar_disponibilidad_aparatos
            )
            btn.pack(side="left", padx=2)
        
       
        self.aparatos_grid = tk.Frame(scrollable_frame, bg=self.card_color)
        self.aparatos_grid.pack(fill="both", expand=True)
        
      
        self.actualizar_disponibilidad_aparatos()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
       
        legend_frame = tk.Frame(card, bg="#f8f9fa", relief="solid", bd=1)
        legend_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(
            legend_frame,
            text="🟢 Disponible  🟡 Parcial  🔴 Ocupado",
            font=("Segoe UI", 8),
            bg="#f8f9fa",
            fg="#2c3e50"
        ).pack(pady=5)
    
    def actualizar_disponibilidad_aparatos(self):
        """Actualiza la visualización de aparatos según el día seleccionado"""
       
        for widget in self.aparatos_grid.winfo_children():
            widget.destroy()
        
        dia = int(self.dia_var.get())
        aparatos = Aparato.listar()
        
        
        aparatos_por_tipo = {}
        for ap in aparatos:
            if ap.tipo not in aparatos_por_tipo:
                aparatos_por_tipo[ap.tipo] = []
            aparatos_por_tipo[ap.tipo].append(ap)
        
        row = 0
        for tipo, lista in sorted(aparatos_por_tipo.items()):
           
            tipo_label = tk.Label(
                self.aparatos_grid,
                text=f"▸ {tipo}",
                font=("Segoe UI", 10, "bold"),
                bg=self.card_color,
                fg="#34495e",
                anchor="w"
            )
            tipo_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10 if row > 0 else 0, 5), padx=5)
            row += 1
            
          
            col = 0
            for ap in lista:
                
                horas_ocupadas = Sesion.horas_ocupadas_por_aparato(ap.id, dia)
                total_franjas = 34  
                ocupacion = len(horas_ocupadas)
                
               
                if ocupacion == 0:
                    color_bg = "#d4edda"
                    color_border = "#28a745"
                    icono = "🟢"
                    estado = "Libre"
                elif ocupacion < 5:
                    color_bg = "#fff3cd" 
                    color_border = "#ffc107"
                    icono = "🟡"
                    estado = f"{ocupacion} reservas"
                else:
                    color_bg = "#f8d7da"  
                    color_border = "#dc3545"
                    icono = "🔴"
                    estado = "Muy ocupado"
                
              
                if tipo == "Cinta":
                    icono_tipo = "🏃"
                elif tipo == "Bicicleta":
                    icono_tipo = "🚴"
                elif tipo in ["Elíptica", "Escaladora"]:
                    icono_tipo = "🔄"
                elif tipo == "Remo":
                    icono_tipo = "🚣"
                elif tipo == "Pesas":
                    icono_tipo = "💪"
                else:
                    icono_tipo = "🏋️"
                
               
                card_frame = tk.Frame(
                    self.aparatos_grid,
                    bg=color_bg,
                    relief="solid",
                    bd=2,
                    highlightbackground=color_border,
                    highlightthickness=1
                )
                card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
                
        
                tk.Label(
                    card_frame,
                    text=f"{icono_tipo} {ap.nombre}",
                    font=("Segoe UI", 9, "bold"),
                    bg=color_bg,
                    fg="#2c3e50"
                ).pack(anchor="w", padx=8, pady=(5, 0))
                
                tk.Label(
                    card_frame,
                    text=f"{icono} {estado}",
                    font=("Segoe UI", 8),
                    bg=color_bg,
                    fg="#495057"
                ).pack(anchor="w", padx=8, pady=(0, 5))
                
               
                btn = tk.Button(
                    card_frame,
                    text="📅 Reservar",
                    font=("Segoe UI", 8, "bold"),
                    bg="#27ae60",
                    fg="white",
                    activebackground="#229954",
                    relief="flat",
                    cursor="hand2",
                    command=lambda a=ap: self.abrir_ventana_reserva(a, "aparato")
                )
                btn.pack(fill="x", padx=5, pady=(0, 5))
                
               
                col = 1 - col
                if col == 0:
                    row += 1
            
           
            if col == 1:
                row += 1
        
        
        self.aparatos_grid.columnconfigure(0, weight=1)
        self.aparatos_grid.columnconfigure(1, weight=1)

    
    def create_clases_section(self, parent):
        """Sección de clases grupales con visualización mejorada"""
        card = tk.Frame(parent, bg=self.card_color, relief="raised", bd=1)
        card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
     
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
        
      
        content_wrapper = tk.Frame(card, bg=self.card_color)
        content_wrapper.pack(fill="both", expand=True, padx=10, pady=10)
        
       
        canvas = tk.Canvas(content_wrapper, bg=self.card_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_wrapper, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.card_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        
        self.clases_grid = tk.Frame(scrollable_frame, bg=self.card_color)
        self.clases_grid.pack(fill="both", expand=True)
        
       
        self.actualizar_disponibilidad_clases()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
       
        legend_frame = tk.Frame(card, bg="#f8f9fa", relief="solid", bd=1)
        legend_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(
            legend_frame,
            text="🟢 Plazas disponibles  🟡 Pocas plazas  🔴 Completo",
            font=("Segoe UI", 8),
            bg="#f8f9fa",
            fg="#2c3e50"
        ).pack(pady=5)
    
    def actualizar_disponibilidad_clases(self):
        """Actualiza la visualización de clases con disponibilidad"""
      
        for widget in self.clases_grid.winfo_children():
            widget.destroy()
        
        clases = Clase.listar()
        
        row = 0
        for clase in clases:
            
            conn = get_db_connection()
            reservas_count = conn.execute("""
                SELECT COUNT(DISTINCT id_cliente) as count
                FROM sesion
                WHERE id_clase = ?
            """, (clase.id,)).fetchone()['count']
            conn.close()
            
            plazas_ocupadas = reservas_count
            plazas_disponibles = clase.capacidad - plazas_ocupadas
            
           
            porcentaje_ocupacion = (plazas_ocupadas / clase.capacidad) * 100 if clase.capacidad > 0 else 100
            
            if porcentaje_ocupacion < 50:
                color_bg = "#d4edda"  
                color_border = "#28a745"
                icono = "🟢"
                estado = f"{plazas_disponibles} plazas libres"
            elif porcentaje_ocupacion < 90:
                color_bg = "#fff3cd"  
                color_border = "#ffc107"
                icono = "🟡"
                estado = f"{plazas_disponibles} plazas"
            else:
                color_bg = "#f8d7da"  
                color_border = "#dc3545"
                icono = "🔴"
                estado = "Casi completo" if plazas_disponibles > 0 else "Completo"
       
            iconos_clase = {
                "Yoga": "🧘",
                "Pilates": "🤸",
                "Spinning": "🚴",
                "Zumba": "💃",
                "CrossFit": "🏋️",
                "Aeróbic": "🤾",
                "Boxeo": "🥊",
                "HIIT": "⚡"
            }
            icono_clase = iconos_clase.get(clase.nombre, "🏃")
            
          
            card_frame = tk.Frame(
                self.clases_grid,
                bg=color_bg,
                relief="solid",
                bd=2,
                highlightbackground=color_border,
                highlightthickness=1
            )
            card_frame.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            
           
            header_frame = tk.Frame(card_frame, bg=color_bg)
            header_frame.pack(fill="x", padx=8, pady=(5, 0))
            
            tk.Label(
                header_frame,
                text=f"{icono_clase} {clase.nombre}",
                font=("Segoe UI", 10, "bold"),
                bg=color_bg,
                fg="#2c3e50"
            ).pack(side="left")
            
            tk.Label(
                header_frame,
                text=f"{icono} {estado}",
                font=("Segoe UI", 8, "bold"),
                bg=color_bg,
                fg="#495057"
            ).pack(side="right")
            
           
            info_frame = tk.Frame(card_frame, bg=color_bg)
            info_frame.pack(fill="x", padx=8, pady=(2, 0))
            
            tk.Label(
                info_frame,
                text=f"👨‍🏫 {clase.instructor}",
                font=("Segoe UI", 8),
                bg=color_bg,
                fg="#495057"
            ).pack(side="left", padx=(0, 10))
            
            tk.Label(
                info_frame,
                text=f"⏱ {clase.duracion_min} min",
                font=("Segoe UI", 8),
                bg=color_bg,
                fg="#495057"
            ).pack(side="left")
            
            tk.Label(
                info_frame,
                text=f"💺 Capacidad: {clase.capacidad}",
                font=("Segoe UI", 8),
                bg=color_bg,
                fg="#495057"
            ).pack(side="left", padx=(10, 0))
            
        
            btn_enabled = plazas_disponibles > 0
            btn_bg = "#9b59b6" if btn_enabled else "#95a5a6"
            btn_hover = "#8e44ad" if btn_enabled else "#95a5a6"
            btn_text = "📝 Reservar" if btn_enabled else "🚫 Completo"
            
            btn = tk.Button(
                card_frame,
                text=btn_text,
                font=("Segoe UI", 8, "bold"),
                bg=btn_bg,
                fg="white",
                activebackground=btn_hover,
                relief="flat",
                cursor="hand2" if btn_enabled else "arrow",
                state="normal" if btn_enabled else "disabled",
                command=lambda c=clase: self.abrir_ventana_reserva(c, "clase")
            )
            btn.pack(fill="x", padx=5, pady=(3, 5))
            
            row += 1
        
       
        self.clases_grid.columnconfigure(0, weight=1)
    
    def create_pagos_section(self, parent):
        """Sección de pagos y cuotas"""
        card = tk.Frame(parent, bg=self.card_color, relief="raised", bd=1)
        card.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        
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
        
      
        content = tk.Frame(card, bg=self.card_color)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
       
        recibos = Recibo.listar_por_cliente(self.usuario.id_cliente)
        pendientes = [r for r in recibos if not r['pagado']]
        pagados = [r for r in recibos if r['pagado']]
        
      
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
        
      
        for r in recibos:
            estado = "✅ Pagado" if r['pagado'] else "❌ Pendiente"
            self.pagos_listbox.insert(tk.END, f"  {r['mes']}/{r['anio']} - €{r['monto']:.2f}")
            self.pagos_listbox.insert(tk.END, f"     {estado}")
            self.pagos_listbox.insert(tk.END, "")
        
        
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
        
     
        tk.Label(
            content,
            text=f"Cuota mensual: €{Recibo.MONTO_MENSUAL:.2f}",
            font=("Segoe UI", 8),
            bg=self.card_color,
            fg="#7f8c8d"
        ).pack(pady=(5, 0))
    
    
    def abrir_ventana_reserva(self, item, tipo):
        """Ventana modal para reservar"""
        ventana = tk.Toplevel(self.window)
        ventana.title(f"Reservar {tipo.capitalize()}")
        ventana.geometry("400x350")
        ventana.resizable(False, False)
        ventana.grab_set()  
        
       
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
        
       
        content = tk.Frame(ventana, bg="white", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
       
        tk.Label(
            content,
            text="Selecciona día y hora:",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 10))
        
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
        
        hora_var = tk.StringVar()
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
            if tipo == "aparato":
                ocupadas = Sesion.horas_ocupadas_por_aparato(item.id, dia)
            else:
                ocupadas = Sesion.horas_ocupadas_por_clase(item.id, dia)
            
            todas_franjas = [f"{h:02d}:{m:02d}" for h in range(6, 23) for m in (0, 30)]
            libres = [h for h in todas_franjas if h not in ocupadas]
            hora_combo['values'] = libres
            hora_combo.set(libres[0] if libres else "")
        
        actualizar_horas()
        
       
        btn_frame = tk.Frame(content, bg="white")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        def confirmar_reserva():
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
                        f"¡Reserva confirmada!\n{dia_a_nombre(dia)} a las {hora}"
                    )
                    ventana.destroy()
                   
                    if tipo == "clase":
                        self.actualizar_disponibilidad_clases()
                    else:
                        self.actualizar_disponibilidad_aparatos()
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
        

        ventana = tk.Toplevel(self.window)
        ventana.title("Pagar Cuota")
        ventana.geometry("400x400")
        ventana.resizable(False, False)
        ventana.grab_set()
        
       
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
        
   
        content = tk.Frame(ventana, bg="white", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Label(
            content,
            text="Selecciona la cuota a pagar:",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 10))
        
        
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