# main.py
from database import init_db
from ui.login import LoginUI
from utils import set_theme, set_window_icon
import tkinter as tk


def main():
    init_db()
    
    root = tk.Tk()
    root.title("🏋️ GymForTheMoment")
    root.geometry("420x580")
    root.resizable(False, False)
    
    # Configurar icono
    set_window_icon(root)
    
    set_theme(root, 'light')
    
    LoginUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()