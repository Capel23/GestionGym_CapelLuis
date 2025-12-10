# ui/cliente_ui.py
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
        self.window.title(f"👋 {usuario.username} | Panel Cliente")
        self.window.geometry("950x620")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Notebook (pestañas)
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestañas
        self.tab_reservar = ttk.Frame(notebook)
        notebook.add(self.tab_reservar, text="📅 Reservar")
        self.setup_reservar_tab()

        self.tab_mis_reservas = ttk.Frame(notebook)
        notebook.add(self.tab_mis_reservas, text="⏳ Mis Reservas")
        self.setup_mis_reservas_tab()

        self.tab_pagos = ttk.Frame(notebook)
        notebook.add(self.tab_pagos, text="💰 Mis Pagos")
        self.setup_pagos_tab()

    def setup_reservar_tab(self):
        frame = ttk.Frame(self.tab_reservar, padding=15)
        frame.pack(fill="both", expand=True)

        # Selector día
        day_frame = ttk.Frame(frame)
        day_frame.pack(fill="x", pady=(0,15))
        ttk.Label(day_frame, text="Día:", font=("Segoe UI", 11, "bold")).pack(side="left")
        self.dia_var = tk.StringVar(value="0")
        dias = [("Lun", "0"), ("Mar", "1"), ("Mié", "2"), ("Jue", "3"), ("Vie", "4")]
        for texto, val in dias:
            ttk.Radiobutton(day_frame, text=texto, variable=self.dia_var, value=val).pack(side="left", padx=8)

        # Aparatos
        ttk.Label(frame, text="Máquinas disponibles:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10,5))
        self.aparato_list = tk.Listbox(frame, height=5, width=50, font=("Consolas", 10))
        self.aparato_list.pack(fill="x", pady=(0,10))
        self.cargar_aparatos()

        # Clases
        ttk.Label(frame, text="Clases grupales:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10,5))
        self.clase_list = tk.Listbox(frame, height=4, width=50, font=("Consolas", 10))
        self.clase_list.pack(fill="x", pady=(0,15))
        self.cargar_clases()

        # Horas libres
        hora_frame = ttk.Frame(frame)
        hora_frame.pack(fill="x")
        ttk.Label(hora_frame, text="Horas libres (30 min):").pack(side="left")
        self.hora_var = tk.StringVar()
        self.hora_combo = ttk.Combobox(hora_frame, textvariable=self.hora_var, state="readonly", width=12)
        self.hora_combo.pack(side="left", padx=(10, 0))

        # Tipo de reserva
        self.tipo_reserva = tk.StringVar(value="aparato")
        ttk.Radiobutton(frame, text="Reservar máquina", variable=self.tipo_reserva, 
                        value="aparato", command=self.actualizar_horas).pack(anchor="w", pady=(5,0))
        ttk.Radiobutton(frame, text="Reservar clase", variable=self.tipo_reserva, 
                        value="clase", command=self.actualizar_horas).pack(anchor="w")

        # Botón
        ttk.Button(frame, text="✅ Reservar", command=self.reservar, width=20).pack(pady=20)

        # Bind selección
        self.aparato_list.bind('<<ListboxSelect>>', self.actualizar_horas)
        self.clase_list.bind('<<ListboxSelect>>', self.actualizar_horas)

    def cargar_aparatos(self):
        aparatos = Aparato.listar()
        self.aparato_list.delete(0, tk.END)
        for ap in aparatos:
            self.aparato_list.insert(tk.END, f"{ap.id} - {ap.nombre} ({ap.tipo})")

    def cargar_clases(self):
        clases = Clase.listar()
        self.clase_list.delete(0, tk.END)
        for c in clases:
            self.clase_list.insert(tk.END, f"{c.id} - {c.nombre} (con {c.instructor})")

    def actualizar_horas(self, event=None):
        dia = int(self.dia_var.get())
        tipo = self.tipo_reserva.get()
        
        ocupadas = []
        if tipo == "aparato":
            try:
                idx = self.aparato_list.curselection()[0]
                linea = self.aparato_list.get(idx)
                id_item = int(linea.split(" - ")[0])
                ocupadas = Sesion.horas_ocupadas_por_aparato(id_item, dia)
            except:
                return
        else:  # clase
            try:
                idx = self.clase_list.curselection()[0]
                linea = self.clase_list.get(idx)
                id_item = int(linea.split(" - ")[0])
                ocupadas = Sesion.horas_ocupadas_por_clase(id_item, dia)
            except:
                return

        # Generar franjas de 30 min
        todas_franjas = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
        libres = [h for h in todas_franjas if h not in ocupadas]
        self.hora_combo['values'] = libres
        self.hora_combo.set(libres[0] if libres else "")

    def reservar(self):
        dia = int(self.dia_var.get())
        hora = self.hora_var.get()
        tipo = self.tipo_reserva.get()
        
        if not hora:
            messagebox.showwarning("⚠️", "Seleccione una hora.")
            return

        try:
            if tipo == "aparato":
                idx = self.aparato_list.curselection()[0]
                linea = self.aparato_list.get(idx)
                id_aparato = int(linea.split(" - ")[0])
                exito = Sesion.reservar(self.usuario.id_cliente, id_aparato=id_aparato, dia_semana=dia, hora_inicio=hora)
            else:
                idx = self.clase_list.curselection()[0]
                linea = self.clase_list.get(idx)
                id_clase = int(linea.split(" - ")[0])
                exito = Sesion.reservar(self.usuario.id_cliente, id_clase=id_clase, dia_semana=dia, hora_inicio=hora)

            if exito:
                messagebox.showinfo("✅", f"Reserva creada para {dia_a_nombre(dia)} a las {hora}.")
                self.actualizar_horas()
            else:
                messagebox.showerror("❌", "Horario ya ocupado. Elige otra franja.")
        except IndexError:
            messagebox.showwarning("⚠️", "Seleccione una máquina o clase.")
        except Exception as e:
            messagebox.showerror("❌", f"Error: {e}")

    def setup_mis_reservas_tab(self):
        frame = ttk.Frame(self.tab_mis_reservas, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Tus próximas reservas", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,15))

        cols = ("Día", "Hora", "Tipo", "Detalle")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for col in cols:
            tree.heading(col, text=col)
            width = 100 if col == "Detalle" else 80
            tree.column(col, width=width)

        sesiones = Sesion.listar_por_cliente(self.usuario.id_cliente)
        for s in sesiones:
            dia = dia_a_nombre(s['dia_semana'])
            tipo = "Máquina" if s['aparato'] else "Clase"
            detalle = s['aparato'] or s['clase'] or "—"
            tree.insert("", "end", values=(dia, s['hora_inicio'], tipo, detalle))

        tree.pack(fill="both", expand=True, pady=(0,20))

    def setup_pagos_tab(self):
        frame = ttk.Frame(self.tab_pagos, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Tus cuotas mensuales", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,15))

        cols = ("Mes", "Año", "Monto", "Estado", "Fecha Pago")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col != "Estado" else 80)

        recibos = Recibo.listar_por_cliente(self.usuario.id_cliente)
        for r in recibos:
            estado = "✅ Pagado" if r['pagado'] else "❌ Pendiente"
            fecha_pago = r['fecha_pago'] or "—"
            tree.insert("", "end", values=(r['mes'], r['anio'], f"€{r['monto']:.2f}", estado, fecha_pago))

        tree.pack(fill="both", expand=True, pady=(0,20))

        def pagar_seleccionado():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("⚠️", "Seleccione un recibo pendiente.")
                return
            item = tree.item(sel[0])
            mes, anio = item['values'][0], item['values'][1]
            if "Pendiente" in item['values'][3]:
                if messagebox.askyesno("💡 Confirmar", f"¿Marcar cuota {mes}/{anio} como pagada?"):
                    Recibo.marcar_pagado(self.usuario.id_cliente, mes, anio)
                    messagebox.showinfo("✅", "Pago registrado.")
                    self.window.destroy()
                    ClientePanel(self.window.master, self.usuario)
            else:
                messagebox.showinfo("ℹ️", "Esta cuota ya está pagada.")

        ttk.Button(frame, text="💳 Marcar como pagado", command=pagar_seleccionado).pack(pady=10)

    def on_close(self):
        self.window.destroy()
        self.window.master.deiconify()