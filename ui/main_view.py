import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio
from modelos.usuario import Usuario
# Vista principal: muestra información, NO lee JSON directamente
class MainView:
    def __init__(self, ventana_padre: tk.Tk, servicio: RestauranteServicio, archivo_servicio, al_cerrar_sesion):
        self.ventana = ventana_padre
        self.servicio = servicio
        self.archivo = archivo_servicio  # Para guardar ventas
        self.al_cerrar_sesion = al_cerrar_sesion

    def mostrar(self, usuario_actual: Usuario):
        # Limpiar vista anterior
        for widget in self.ventana.winfo_children():
            widget.destroy()
        self.usuario_actual = usuario_actual
        self.ventana.title(f"Restaurante App — Bienvenido/a {usuario_actual.nombre}")
        self.ventana.geometry("720x500")

        # Barra superior
        barra = ttk.Frame(self.ventana, padding=10)
        barra.pack(fill=tk.X)
        ttk.Label(barra, text=f"👤 Usuario: {usuario_actual.nombre} ({usuario_actual.identificacion})",
                  font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        ttk.Button(barra, text="Cerrar sesión", command=self.al_cerrar_sesion).pack(side=tk.RIGHT)

        # Pestañas
        cuaderno = ttk.Notebook(self.ventana)
        cuaderno.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))

        # Pestaña Productos
        pestaña_prod = ttk.Frame(cuaderno, padding=10)
        cuaderno.add(pestaña_prod, text=f"📦 Productos ({self.servicio.cantidad_productos()})")
        self._construir_tabla_productos(pestaña_prod)

        # Pestaña Usuarios 
        pestaña_usu = ttk.Frame(cuaderno, padding=10)
        cuaderno.add(pestaña_usu, text=f"👥 Usuarios ({self.servicio.cantidad_usuarios()})")
        self._construir_tabla_usuarios(pestaña_usu)

        # Pestaña Ventas 
        pestaña_ventas = ttk.Frame(cuaderno, padding=10)
        cuaderno.add(pestaña_ventas, text="💰 Ventas")
        self._construir_pestana_ventas(pestaña_ventas)

    def _construir_tabla_productos(self, marco):
        columnas = ("codigo", "nombre", "precio", "stock")
        tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=12)
        tabla.heading("codigo", text="Código")
        tabla.heading("nombre", text="Nombre")
        tabla.heading("precio", text="Precio")
        tabla.heading("stock", text="Stock")
        tabla.column("codigo", width=90)
        tabla.column("nombre", width=300)
        tabla.column("precio", width=110)
        tabla.column("stock", width=90)
        tabla.pack(expand=True, fill=tk.BOTH)
        for prod in self.servicio.listar_productos():
            tabla.insert("", tk.END, values=(prod.codigo, prod.nombre, f"${prod.precio:.2f}", prod.stock))

    def _construir_tabla_usuarios(self, marco):
        columnas = ("id", "nombre")
        tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=12)
        tabla.heading("id", text="Identificación")
        tabla.heading("nombre", text="Nombre Completo")
        tabla.column("id", width=180)
        tabla.column("nombre", width=400)
        tabla.pack(expand=True, fill=tk.BOTH)
        for usu in self.servicio.listar_usuarios():
            tabla.insert("", tk.END, values=(usu.identificacion, usu.nombre))

    # ==============================================================
    # Pestaña de Ventas
    # ==============================================================
    def _construir_pestana_ventas(self, marco):
        ttk.Label(marco, text="Registro de Ventas", font=("Arial", 12, "bold")).pack(pady=5)

        # Formulario de selección
        form = ttk.LabelFrame(marco, text="Datos de la Venta", padding=10)
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cmb_venta_usuario = ttk.Combobox(form, state="readonly", width=35)
        self.cmb_venta_usuario.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Producto:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cmb_venta_producto = ttk.Combobox(form, state="readonly", width=35)
        self.cmb_venta_producto.grid(row=1, column=1, padx=5, pady=5)

        self._cargar_listas_venta()

        # Paso la referencia del método
        ttk.Button(form, text="Registrar Venta",
                   command=self._al_registrar_venta).grid(row=2, column=0, columnspan=2, pady=10)

        # Tabla de ventas registradas
        ttk.Label(marco, text="Ventas Registradas", font=("Arial", 10, "bold")).pack(pady=5)
        columnas = ("id", "usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(marco, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tabla_ventas.heading(col, text=col.title())
            self.tabla_ventas.column(col, width=130)
        self.tabla_ventas.pack(fill="both", expand=True)

        self._refrescar_tabla_ventas()

    def _cargar_listas_venta(self):
        # Mapeo: nombre visible → código real
        self._mapa_usuarios = {u.nombre: u.identificacion for u in self.servicio.listar_usuarios()}
        self.cmb_venta_usuario["values"] = list(self._mapa_usuarios.keys())

        self._mapa_productos = {p.nombre: p.codigo for p in self.servicio.listar_productos()}
        self.cmb_venta_producto["values"] = list(self._mapa_productos.keys())

    # CALLBACK — Semana 15: coordina toda la acción
    def _al_registrar_venta(self):
        nombre_usuario = self.cmb_venta_usuario.get()
        nombre_producto = self.cmb_venta_producto.get()

        if not nombre_usuario or not nombre_producto:
            messagebox.showwarning("Aviso", "Seleccione un usuario y un producto")
            return

        usuario_id = self._mapa_usuarios[nombre_usuario]
        producto_codigo = self._mapa_productos[nombre_producto]

        try:
            # Delegar lógica al servicio
            self.servicio.registrar_venta(usuario_id, producto_codigo)
            # Guardar en archivo JSON
            self.archivo.guardar_ventas(self.servicio.listar_ventas())
            messagebox.showinfo("Éxito", "Venta registrada correctamente")
            # Limpiar selección
            self.cmb_venta_usuario.set("")
            self.cmb_venta_producto.set("")
            # Actualizar tabla
            self._refrescar_tabla_ventas()
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def _refrescar_tabla_ventas(self):
        # Limpiar filas existentes
        for fila in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(fila)

        ventas = self.servicio.listar_ventas()
        if not ventas:
            return

        # Convertir códigos a nombres para mostrar
        nom_usu = {u.identificacion: u.nombre for u in self.servicio.listar_usuarios()}
        nom_prod = {p.codigo: p.nombre for p in self.servicio.listar_productos()}

        # Llenar tabla
        for v in ventas:
            self.tabla_ventas.insert("", "end", values=(
                v.identificador,
                nom_usu.get(v.usuario_id, "Desconocido"),
                nom_prod.get(v.producto_codigo, "Desconocido"),
                v.fecha
            ))