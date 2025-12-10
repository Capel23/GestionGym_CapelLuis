# main.py
from database import init_db
from ui.login import LoginUI
from utils import set_theme
import tkinter as tk
import os
from pathlib import Path

def main():
    init_db()
    
    root = tk.Tk()
    root.title("🏋️ GymForTheMoment")
    root.geometry("420x580")
    root.resizable(False, False)
    
    icon_path = Path(__file__).parent / "assets" / "gym_icon.ico"
    if icon_path.exists():
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print(f"⚠️ No se pudo cargar el icono: {e}")
    
    set_theme(root, 'light')
    
    LoginUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()