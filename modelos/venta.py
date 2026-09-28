class Venta:
    """Modelo de Venta — Semana 15."""

    def __init__(self, identificador, usuario_id, producto_codigo, fecha):
        self.identificador = identificador
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.fecha = fecha

    def to_dict(self):
        return {
            "identificador": self.identificador,
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "fecha": self.fecha
        }
        