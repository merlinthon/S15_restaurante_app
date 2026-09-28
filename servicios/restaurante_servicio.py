from datetime import date
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

# Aquí reside TODA la lógica de negocio. Las vistas SOLO llaman a este servicio
class RestauranteServicio:
    def __init__(self, productos: list[Producto], usuarios: list[Usuario], ventas: list[Venta] | None = None) -> None:
        # Recibo los datos desde main.py, NO los leo directamente aquí
        self._productos = productos
        self._usuarios = usuarios
        self._ventas = ventas if ventas is not None else []
        # Índice para acceso rápido
        self._usuarios_por_id = {u.identificacion: u for u in usuarios}
        # Índices para ventas
        self._productos_por_codigo = {p.codigo: p for p in productos}


    def validar_acceso(self, identificacion: str, contraseña: str) -> Usuario | None:
        """Simulación de acceso pedagógica: valida sin encriptar."""
        identificacion = identificacion.strip()
        contraseña = contraseña.strip()
        if not identificacion or not contraseña:
            return None
        usuario = self._usuarios_por_id.get(identificacion)
        if usuario and usuario.contraseña == contraseña:
            return usuario
        return None

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)

    # ==============================================================
    # Operaciones de Ventas
    # ==============================================================
    def generar_id_venta(self) -> str:
        return f"V{str(len(self._ventas) + 1).zfill(3)}"

    def registrar_venta(self, usuario_id: str, producto_codigo: str) -> Venta:
        # Validar usuario
        usuario = self._usuarios_por_id.get(usuario_id)
        if not usuario:
            raise ValueError("El usuario seleccionado no existe")

        # Validar producto
        producto = self._productos_por_codigo.get(producto_codigo)
        if not producto:
            raise ValueError("El producto seleccionado no existe")

        # Crear venta
        nueva_venta = Venta(
            identificador=self.generar_id_venta(),
            usuario_id=usuario_id,
            producto_codigo=producto_codigo,
            fecha=date.today().isoformat()
        )
        self._ventas.append(nueva_venta)
        return nueva_venta

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()