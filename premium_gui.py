import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta, timezone
import tkinter as tk
from tkinter import messagebox
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta al recurso (para PyInstaller y desarrollo)."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

# Inicializar Firebase desde archivo empaquetado o local
cred_path = resource_path("firebase-key.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def otorgar_premium():
    user_id = entry_user.get().strip()
    try:
        days = int(entry_days.get().strip())
    except ValueError:
        days = 30  # valor por defecto

    if not user_id.isdigit():
        messagebox.showerror("Error", "El ID debe ser numérico.")
        return

    premium_until = datetime.now(timezone.utc) + timedelta(days=days)
    premium_iso = premium_until.isoformat().replace("+00:00", "Z")

    db.collection("users").document(user_id).set({
        "premium_until": premium_iso
    }, merge=True)

    messagebox.showinfo("Éxito", f"Premium activado hasta:\n{premium_iso}")

# GUI
ventana = tk.Tk()
ventana.title("Otorgar Premium")
ventana.geometry("300x180")
ventana.resizable(False, False)

tk.Label(ventana, text="ID del usuario:").pack(pady=(10, 0))
entry_user = tk.Entry(ventana)
entry_user.pack()

tk.Label(ventana, text="Días de Premium:").pack(pady=(10, 0))
entry_days = tk.Entry(ventana)
entry_days.insert(0, "30")
entry_days.pack()

tk.Button(ventana, text="Otorgar Premium", command=otorgar_premium).pack(pady=15)

ventana.mainloop()
