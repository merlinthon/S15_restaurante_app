import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio

# LoginView SOLO se encarga de mostrar pantalla de acceso, NO lee archivos
class LoginView:
    def __init__(self, ventana_padre: tk.Tk, servicio: RestauranteServicio, al_ingresar):
        self.ventana = ventana_padre
        self.servicio = servicio
        self.al_ingresar = al_ingresar  # Función a ejecutar si acceso es válido

    def mostrar(self):
        # Limpio cualquier contenido anterior de la ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        self.ventana.title("Acceso — Restaurante App")
        self.ventana.geometry("420x320")
        self.ventana.resizable(False, False)

        # Contenedor centrado
        marco = ttk.Frame(self.ventana, padding=40)
        marco.pack(expand=True, fill=tk.BOTH)

        ttk.Label(marco, text="🍽️  Restaurante App", font=("Arial", 16, "bold")).pack(pady=(0, 30))

        ttk.Label(marco, text="Usuario / Identificación:").pack(anchor=tk.W)
        self.campo_usuario = ttk.Entry(marco, font=("Arial", 11))
        self.campo_usuario.pack(fill=tk.X, pady=(5, 15))

        ttk.Label(marco, text="Contraseña:").pack(anchor=tk.W)
        self.campo_clave = ttk.Entry(marco, show="•", font=("Arial", 11))
        self.campo_clave.pack(fill=tk.X, pady=(5, 20))

        ttk.Button(marco, text="Ingresar", command=self._al_pulsar_ingresar).pack(fill=tk.X, pady=10)

    def _al_pulsar_ingresar(self):
        usuario = self.campo_usuario.get()
        clave = self.campo_clave.get()

        # La validación se delega al servicio, NO se hace aquí
        acceso = self.servicio.validar_acceso(usuario, clave)

        if not usuario.strip() or not clave.strip():
            messagebox.showwarning("Datos incompletos", "Por favor complete ambos campos.")
            return

        if acceso:
            self.al_ingresar(acceso)  # Cambiar a vista principal
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
            self.campo_clave.delete(0, tk.END)