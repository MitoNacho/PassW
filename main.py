import tkinter as tk
from tkinter import messagebox
import random
import string
import json

def generar_contrasena(longitud, complejidad):
    caracteres = ''
    if complejidad == 'baja':
        caracteres = string.ascii_lowercase + string.digits                       # --- Letras minúsculas y números ---
    elif complejidad == 'media':
        caracteres = string.ascii_letters + string.digits                         # --- Letras minúsculas, mayúsculas y números ---
    elif complejidad == 'alta':
        caracteres = string.ascii_letters + string.digits + string.punctuation    # --- Añade signos de puntuación ---

    return ''.join(random.choice(caracteres) for _ in range(longitud))

def guardar_contrasenas(contrasenas):
    try:
        with open('contrasenas.txt', 'r') as archivo:
            data = json.load(archivo)
    except FileNotFoundError:
        data = {}

    data.update(contrasenas)
    with open('contrasenas.txt', 'w') as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)

def generar_y_mostrar_contrasena():
    try:
        longitud = int(longitud_entry.get())
        complejidad = complejidad_var.get()
        sitio = sitio_entry.get()

        if not sitio:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un sitio o servicio.")
            return

        nueva = generar_contrasena(longitud, complejidad)
        resultado_label.config(text=nueva)
        contrasenas_guardadas[sitio] = nueva

    except ValueError:
        messagebox.showerror("Error", "La longitud debe ser un número entero.")

def guardar_contrasena_actual():
    sitio = sitio_entry.get()
    contrasena = resultado_label.cget("text").split(":")[-1].strip()

    if sitio and contrasena:
        guardar_contrasenas({sitio: contrasena})
        sitio_entry.delete(0, tk.END)
        longitud_entry.delete(0, tk.END)
        resultado_label.config(text="Contraseña guardada ✅")
    else:
        resultado_label.config(text="Por favor genera una contraseña primero.")


def salir_del_programa():
    root.destroy()

def copiar_al_portapapeles():
    contrasena = resultado_label.cget("text")
    if contrasena:
        root.clipboard_clear()
        root.clipboard_append(contrasena)
        messagebox.showinfo("Copiada", "Contraseña copiada al portapapeles.")

# --- Interfaz ---
root = tk.Tk()
root.title("🔐 Generador de Contraseñas")
root.geometry("400x400")
root.configure(bg="#fdffb6")

contrasenas_guardadas = {}

tk.Label(root, text="PassW", font=("Helvetica", 28, "bold"), bg="#fdffb6").pack(pady=10)

form_frame = tk.Frame(root, bg="#fdffb6")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Sitio / Servicio:", bg="#fdffb6").grid(row=0, column=0, sticky="e", pady=5)
sitio_entry = tk.Entry(form_frame)
sitio_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Longitud:", bg="#fdffb6").grid(row=1, column=0, sticky="e", pady=5)
longitud_entry = tk.Entry(form_frame)
longitud_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Complejidad:", bg="#fdffb6").grid(row=2, column=0, sticky="e", pady=5)
complejidad_var = tk.StringVar(value="baja")
complejidad_menu = tk.OptionMenu(form_frame, complejidad_var, "baja", "media", "alta")
complejidad_menu.grid(row=2, column=1, pady=5,)

tk.Button(root, text="Generar Contraseña", bg="#caffbf", fg="black", command=generar_y_mostrar_contrasena).pack(pady=10)

tk.Label(root, text="Contraseña Generada:", bg="#fdffb6", font=("Helvetica", 10, "bold")).pack()
resultado_label = tk.Label(root, text="", font=("Courier", 14), bg="white", width=30, relief="sunken", pady=5)
resultado_label.pack(pady=5)

tk.Button(root, text="Copiar al portapapeles", bg="#ffd6a5" , command=copiar_al_portapapeles).pack(pady=5)
botones_frame = tk.Frame(root, bg='#fdffb6')
botones_frame.pack(pady=10)

guardar_button = tk.Button(botones_frame, text="Guardar", bg="#9bf6ff" , command=guardar_contrasena_actual)
guardar_button.pack(side=tk.LEFT, padx=5)

salir_button = tk.Button(botones_frame, text="Salir", bg="#ffadad" , command=salir_del_programa)
salir_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
