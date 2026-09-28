import json
from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta  

# Esta capa SOLO lee y escribe JSON. Nunca debe conocer nada de la interfaz
class ArchivoServicio:
    def __init__(self, ruta_datos: str = "datos") -> None:
        self._ruta_datos = Path(ruta_datos)
        self._ruta_productos = self._ruta_datos / "productos.json"
        self._ruta_usuarios = self._ruta_datos / "usuarios.json"
        self._ruta_ventas = self._ruta_datos / "ventas.json" 

    def cargar_productos(self) -> list[Producto]:
        datos = self._leer_lista(self._ruta_productos, "productos")
        productos = []
        for item in datos:
            try:
                productos.append(Producto(
                    item["codigo"],
                    item["nombre"],
                    item["precio"],
                    item.get("stock", 0),
                ))
            except (KeyError, ValueError):
                continue
        return productos

    def cargar_usuarios(self) -> list[Usuario]:
        datos = self._leer_lista(self._ruta_usuarios, "usuarios")
        usuarios = []
        for item in datos:
            try:
                usuarios.append(Usuario(
                    item["identificacion"],
                    item["nombre"],
                    item.get("contraseña", ""),
                ))
            except (KeyError, ValueError):
                continue
        return usuarios

    # NUEVO: Cargar ventas
    def cargar_ventas(self) -> list[Venta]:
        datos = self._leer_lista(self._ruta_ventas, "ventas")
        ventas = []
        for item in datos:
            try:
                ventas.append(Venta(
                    item["identificador"],
                    item["usuario_id"],
                    item["producto_codigo"],
                    item["fecha"],
                ))
            except (KeyError, ValueError):
                continue
        return ventas

    # NUEVO: Guardar ventas
    def guardar_ventas(self, ventas: list[Venta]) -> None:
        self._escribir_lista(self._ruta_ventas, [v.to_dict() for v in ventas])

    def _leer_lista(self, ruta: Path, nombre: str) -> list:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"El archivo de {nombre} tiene formato inválido.")
            return []
        return datos if isinstance(datos, list) else []

    # NUEVO: Escribir lista (reutilizable)
    def _escribir_lista(self, ruta: Path, datos: list) -> None:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)