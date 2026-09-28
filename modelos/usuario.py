# Mantengo Usuario con contraseña para la simulación de acceso pedagógica
class Usuario:
    def __init__(self, identificacion: str, nombre: str, contraseña: str) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.contraseña = contraseña

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificación no puede estar vacía.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def contraseña(self) -> str:
        return self._contraseña

    @contraseña.setter
    def contraseña(self, valor: str) -> None:
        if valor is None:
            valor = ""
        self._contraseña = valor

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "contraseña": self.contraseña,
        }

    def __str__(self) -> str:
        return f"ID: {self.identificacion} | Nombre: {self.nombre}"