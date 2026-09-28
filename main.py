from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView
import tkinter as tk

def main():
    # Cargar capas
    archivo = ArchivoServicio("datos")
    productos = archivo.cargar_productos()
    usuarios = archivo.cargar_usuarios()
    ventas = archivo.cargar_ventas()

    # Pasar TODO al servicio
    servicio = RestauranteServicio(productos, usuarios, ventas)
    # Ventana
    raiz = tk.Tk()
    raiz.title("Restaurante App — Semana 15")
    raiz.geometry("800x550")

    def al_iniciar_sesion(usuario):
        for hijo in raiz.winfo_children():
            hijo.destroy()
        MainView(raiz, servicio, usuario, archivo)

    LoginView(raiz, servicio, al_iniciar_sesion)
    raiz.mainloop()

if __name__ == "__main__":
    main()