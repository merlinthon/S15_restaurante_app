# Restaurante App — Semana 15

**Estudiante:** Merlinthon Wilfrido España Carbo  

> Asignatura: Programación Orientada a Objetos

---

## Propósito


## Estructura del Proyecto

```text
Repositorio GitHub
├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json
│   │   ├── usuarios.json
│   │   └── ventas.json
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── usuario.py
│   │   └── venta.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py
│   │   └── restaurante_servicio.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   └── main_view.py
│   ├── assets/              (obligatorio: íconos, logo/logotipo y recursos visuales)
│   └── main.py
└── README.md
```
---

## Flujo de la Aplicación
*modelos/:* Definen las entidades con sus atributos y conversión a diccionario. No conocen archivos ni interfaz.
*servicios/archivo_servicio.py:* Única capa que lee y escribe archivos JSON. No valida ni procesa datos.
*servicios/restaurante_servicio.py:* Contiene las reglas de negocio, validaciones y operaciones. La interfaz solo llama a métodos de esta clase.
*ui/:* Construye la interfaz gráfica y captura acciones del usuario. Nunca modifica archivos directamente.
*main.py:* Conecta todas las capas, carga los datos y muestra la ventana de inicio.

## Conceptos clave aplicados
**Callback sin paréntesis:** command=self._al_registrar_venta pasa la referencia del método; se ejecuta solo al hacer clic, no al crear el botón.
**Separación de responsabilidades:** La vista no conoce la ubicación de los archivos ni la estructura de los datos.
**Persistencia:** ventas.json puede estar vacío [] sin causar errores; se inicializa como lista vacía automáticamente.
**Actualización reactiva:** Después de guardar, la tabla se recarga sin reiniciar la aplicación.

## Funcionalidades
📦 Productos:	Consulta de productos registrados (heredado de S14)
👥 Usuarios:	Consulta de usuarios del sistema (heredado de S14)
💰 Ventas:	Selección de usuario y producto → registro → persistencia → visualización

## Reflexión del Aprendizaje
Durante el desarrollo de esta semana comprendí que una interfaz gráfica no debe mezclarse con la lógica de negocio. Al principio me confundía el uso de los paréntesis en command=, pero al probarlo entendí la diferencia entre pasar la referencia de un método y ejecutarlo de inmediato.
La estructura modular me ayudó mucho: cuando tuve que agregar la funcionalidad de ventas, no modifiqué lo que ya funcionaba de productos y usuarios, solo sumé nuevas clases y métodos respetando lo construido en semanas anteriores. Esto demuestra que la planificación y la separación de responsabilidades hacen que el código sea más fácil de ampliar y corregir.
Enfrenté dificultades con la carga inicial de ventas.json cuando estaba vacío; resolverlo me enseñó la importancia de prever casos en los que no hay datos y garantizar que el sistema no se interrumpa. Aprendí también que cada capa tiene su tarea bien definida: la vista muestra, el servicio decide y el archivo guarda. Mantener esta disciplina facilita mucho el mantenimiento del programa.
