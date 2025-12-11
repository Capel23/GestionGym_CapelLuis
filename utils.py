import tkinter as tk
from tkinter import ttk
import re
from pathlib import Path

THEMES = {
    'light': {
        'bg': '#F8F9FA',
        'fg': '#212529',
        'accent': '#3498DB',
        'success': '#2ECC71',
        'danger': '#E74C3C',
        'border': '#CED4DA',
        'entry_bg': 'white',
        'entry_fg': 'black'
    },
    'dark': {
        'bg': '#2D2D2D',
        'fg': '#E0E0E0',
        'accent': '#3498DB',
        'success': '#2ECC71',
        'danger': '#E74C3C',
        'border': '#444444',
        'entry_bg': '#3C3C3C',
        'entry_fg': '#E0E0E0'
    }
}

_current_theme = 'light'

def set_theme(root, theme='light'):
    """Aplica el tema a la ventana raíz y widgets ttk."""
    global _current_theme
    _current_theme = theme
    colors = THEMES[theme]
    
    style = ttk.Style()
    style.theme_use('clam')
    
    root.configure(bg=colors['bg'])
    
    style.configure('TFrame', background=colors['bg'])
    style.configure('TLabel', background=colors['bg'], foreground=colors['fg'])
    style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground=colors['accent'])
    style.configure('Sub.TLabel', font=('Segoe UI', 10), foreground='#7F8C8D', background=colors['bg'])
    style.configure('TButton', font=('Segoe UI', 11), padding=6)
    style.map('TButton',
        background=[('active', colors['accent'])],
        foreground=[('active', 'white')]
    )
    style.configure('TEntry',
        fieldbackground=colors['entry_bg'],
        foreground=colors['entry_fg'],
        bordercolor=colors['border']
    )
    style.configure('TCombobox',
        fieldbackground=colors['entry_bg'],
        foreground=colors['entry_fg']
    )

def toggle_theme(root):
    """Alterna entre tema claro y oscuro."""
    global _current_theme
    new_theme = 'dark' if _current_theme == 'light' else 'light'
    set_theme(root, new_theme)

def validar_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

def validar_usuario(user):
    return 3 <= len(user) <= 20 and re.match(r"^\w+$", user)

def validar_hora_30min(hora):
    return bool(re.match(r"^([01]?[0-9]|2[0-3]):[03]0$", hora))

def dia_a_nombre(dia):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    return dias[dia] if 0 <= dia <= 4 else "Desconocido"

def set_window_icon(window):
    """Configura el icono del gimnasio en la ventana proporcionada.
    
    Args:
        window: Instancia de tk.Tk o tk.Toplevel
    """
    try:
        # Buscar el icono en la carpeta assets
        # Si window es Toplevel, necesitamos buscar desde la raíz del proyecto
        if hasattr(window, 'master') and window.master:
            # Es un Toplevel, buscar desde el directorio del script principal
            icon_path = Path(__file__).parent.parent / "assets" / "gym_icon.ico"
        else:
            # Es la ventana raíz
            icon_path = Path(__file__).parent / "assets" / "gym_icon.ico"
        
        if icon_path.exists():
            window.iconbitmap(icon_path)
        else:
            print(f"⚠️ Icono no encontrado en: {icon_path}")
    except Exception as e:
        print(f"⚠️ No se pudo cargar el icono: {e}")