import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class InterfazPrincipal:
    def __init__(self, raiz, servicio, usuario_actual, archivo_servicio):
        self.raiz = raiz
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.archivo = archivo_servicio

        self.raiz.title("Restaurante App")
        self.raiz.geometry("1200x700")
        self.raiz.minsize(1000, 600)
        self.raiz.configure(bg="#f4f4f4")

        self.cuaderno = ttk.Notebook(self.raiz)
        self.cuaderno.pack(fill="both", expand=True, padx=10, pady=10)

        self.pestana_inicio = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pestana_inicio, text="Inicio")
        self._construir_inicio()

        self.pestana_productos = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pestana_productos, text="Productos")
        self._construir_productos()

        self.pestana_mesas = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pestana_mesas, text="Mesas")
        self._construir_mesas()

        self.pestana_ventas = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pestana_ventas, text="Ventas")
        self._construir_ventas()

    def _construir_inicio(self):
        lbl = ttk.Label(
            self.pestana_inicio,
            text=f"Bienvenido(a), {self.usuario_actual}",
            font=("Arial", 16, "bold"),
        )
        lbl.pack(padx=20, pady=(30, 10))

        resumen = ttk.Label(
            self.pestana_inicio,
            text="Sistema de gestión del restaurante",
            font=("Arial", 11),
        )
        resumen.pack(padx=20, pady=10)

        info = ttk.Label(
            self.pestana_inicio,
            text="Desde aquí puedes administrar productos, mesas y ventas.",
            justify="left",
        )
        info.pack(padx=20, pady=10, anchor="w")

    def _construir_productos(self):
        frame = ttk.Frame(self.pestana_productos, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Productos", font=("Arial", 12, "bold")).pack(anchor="w")

        self.tree_productos = ttk.Treeview(
            frame,
            columns=("codigo", "nombre", "precio", "categoria"),
            show="headings",
            height=16,
        )
        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Nombre")
        self.tree_productos.heading("precio", text="Precio")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.column("codigo", width=100, anchor="center")
        self.tree_productos.column("nombre", width=250)
        self.tree_productos.column("precio", width=120, anchor="center")
        self.tree_productos.column("categoria", width=180)
        self.tree_productos.pack(fill="both", expand=True, pady=(10, 0))

        self._cargar_productos()

    def _construir_mesas(self):
        frame = ttk.Frame(self.pestana_mesas, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Mesas", font=("Arial", 12, "bold")).pack(anchor="w")

        self.tree_mesas = ttk.Treeview(
            frame,
            columns=("numero", "estado", "cliente"),
            show="headings",
            height=16,
        )
        self.tree_mesas.heading("numero", text="Número")
        self.tree_mesas.heading("estado", text="Estado")
        self.tree_mesas.heading("cliente", text="Cliente")
        self.tree_mesas.column("numero", width=120, anchor="center")
        self.tree_mesas.column("estado", width=180, anchor="center")
        self.tree_mesas.column("cliente", width=260)
        self.tree_mesas.pack(fill="both", expand=True, pady=(10, 0))

        self._cargar_mesas()

    def _construir_ventas(self):
        panel = ttk.Frame(self.pestana_ventas, padding=12)
        panel.pack(fill="both", expand=True)

        form = ttk.LabelFrame(panel, text="Registrar venta", padding=10)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Producto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.venta_producto = ttk.Entry(form, width=30)
        self.venta_producto.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.venta_cantidad = ttk.Entry(form, width=12)
        self.venta_cantidad.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Cliente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.venta_cliente = ttk.Entry(form, width=30)
        self.venta_cliente.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Método:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.venta_metodo = ttk.Combobox(form, state="readonly", width=18, values=["Efectivo", "Tarjeta", "Transferencia"])
        self.venta_metodo.grid(row=1, column=3, padx=5, pady=5)
        self.venta_metodo.current(0)

        btn_guardar = ttk.Button(form, text="Guardar venta", command=self._registrar_venta)
        btn_guardar.grid(row=2, column=0, columnspan=4, pady=(10, 0), sticky="ew")

        tabla = ttk.LabelFrame(panel, text="Ventas realizadas", padding=10)
        tabla.pack(fill="both", expand=True)

        self.tree_ventas = ttk.Treeview(
            tabla,
            columns=("fecha", "producto", "cantidad", "cliente", "monto", "usuario", "metodo"),
            show="headings",
            height=15,
        )
        self.tree_ventas.heading("fecha", text="Fecha")
        self.tree_ventas.heading("producto", text="Producto")
        self.tree_ventas.heading("cantidad", text="Cantidad")
        self.tree_ventas.heading("cliente", text="Cliente")
        self.tree_ventas.heading("monto", text="Monto")
        self.tree_ventas.heading("usuario", text="Usuario")
        self.tree_ventas.heading("metodo", text="Método")

        self.tree_ventas.column("fecha", width=120, anchor="center")
        self.tree_ventas.column("producto", width=180)
        self.tree_ventas.column("cantidad", width=90, anchor="center")
        self.tree_ventas.column("cliente", width=150)
        self.tree_ventas.column("monto", width=100, anchor="center")
        self.tree_ventas.column("usuario", width=120)
        self.tree_ventas.column("metodo", width=115, anchor="center")
        self.tree_ventas.pack(fill="both", expand=True)

        self._cargar_ventas()

    def _cargar_productos(self):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        try:
            if hasattr(self.servicio, "listar_productos"):
                productos = self.servicio.listar_productos()
                for p in productos:
                    self.tree_productos.insert(
                        "",
                        "end",
                        values=(
                            p.get("codigo", ""),
                            p.get("nombre", ""),
                            p.get("precio", ""),
                            p.get("categoria", ""),
                        ),
                    )
        except Exception:
            pass

    def _cargar_mesas(self):
        for item in self.tree_mesas.get_children():
            self.tree_mesas.delete(item)

        try:
            if hasattr(self.servicio, "listar_mesas"):
                mesas = self.servicio.listar_mesas()
                for m in mesas:
                    self.tree_mesas.insert(
                        "",
                        "end",
                        values=(
                            m.get("numero", ""),
                            m.get("estado", ""),
                            m.get("cliente", ""),
                        ),
                    )
        except Exception:
            pass

    def _cargar_ventas(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        try:
            ventas = []
            if hasattr(self.servicio, "listar_ventas"):
                ventas = self.servicio.listar_ventas()
            elif hasattr(self.servicio, "obtener_ventas"):
                ventas = self.servicio.obtener_ventas()

            for v in ventas:
                self.tree_ventas.insert(
                    "",
                    "end",
                    values=(
                        v.get("fecha", ""),
                        v.get("producto", ""),
                        v.get("cantidad", ""),
                        v.get("cliente", ""),
                        v.get("monto", ""),
                        v.get("usuario", ""),
                        v.get("metodo", ""),
                    ),
                )
        except Exception:
            pass

    def _registrar_venta(self):
        producto = self.venta_producto.get().strip()
        cantidad = self.venta_cantidad.get().strip()
        cliente = self.venta_cliente.get().strip()
        metodo = self.venta_metodo.get()

        if not producto or not cantidad or not cliente:
            messagebox.showwarning("Datos incompletos", "Completa producto, cantidad y cliente.")
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Cantidad inválida", "La cantidad debe ser un número entero.")
            return

        datos = {
            "producto": producto,
            "cantidad": cantidad,
            "cliente": cliente,
            "metodo": metodo,
            "usuario": self.usuario_actual,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        try:
            if hasattr(self.servicio, "registrar_venta"):
                self.servicio.registrar_venta(datos)
            elif hasattr(self.servicio, "guardar_venta"):
                self.servicio.guardar_venta(datos)
            else:
                self._guardar_venta_local(datos)
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo guardar la venta: {exc}")
            return

        self.venta_producto.delete(0, tk.END)
        self.venta_cantidad.delete(0, tk.END)
        self.venta_cliente.delete(0, tk.END)
        self.venta_metodo.current(0)
        self._cargar_ventas()
        messagebox.showinfo("Venta registrada", "La venta se guardó correctamente.")

    def _guardar_venta_local(self, datos):
        ventas = []
        try:
            import json
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                ventas = json.load(archivo)
        except Exception:
            ventas = []

        ventas.append({
            "fecha": datos["fecha"],
            "producto": datos["producto"],
            "cantidad": datos["cantidad"],
            "cliente": datos["cliente"],
            "monto": 0,
            "usuario": datos["usuario"],
            "metodo": datos["metodo"],
        })

        import json
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(ventas, archivo, ensure_ascii=False, indent=2)
