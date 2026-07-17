# SPEC.md — CLI Todo List

## Descripción general
Herramienta ligera de terminal para gestionar tareas desde la línea de comandos. Desarrollada en Python 3 sin dependencias externas.

## Funcionalidades
1. **Agregar tarea** — Añade una nueva tarea al final de la lista proporcionando su título.
2. **Listar tareas** — Muestra todas las tareas enumeradas con posición numérica (1, 2, 3…).
3. **Eliminar tarea** — Borra una tarea indicando su número de posición.
4. **Persistencia en CSV** — Guarda y carga automáticamente desde `todos.csv`.
5. **Sin edición** — No se permite modificar el título de una tarea existente.

## Tecnología
- **Lenguaje:** Python 3 (solo biblioteca estándar)
- **Interfaz:** Menú interactivo en terminal

## Especificación detallada

### Carga inicial (`load_todos`)
- Al iniciar el programa se lee `todos.csv` del mismo directorio.
- Si el archivo no existe, se parte de una lista vacía.
- La primera línea del CSV es la cabecera (`titulo`). Se ignora al cargar.
- Cada línea siguiente contiene un título de tarea.

### Persistencia (`save_todos`)
- Se guarda inmediatamente después de cada operación (agregar o eliminar).
- Formato CSV con una sola columna: `titulo`.
- Se escribe con cabecera (`titulo\n`).

### Agregar tarea (`add_one_task`)
- Recibe el título por parámetro.
- No se permiten títulos vacíos → muestra error y no guarda.
- Sí se permiten duplicados.
- La tarea se agrega al final de la lista.

### Listar tareas (`print_list`)
- Muestra cada tarea en el formato: `{posicion}. {titulo}`
- La numeración empieza en 1.
- Si no hay tareas, muestra mensaje indicando que la lista está vacía.

### Eliminar tarea (`delete_task`)
- Recibe la posición por parámetro (entero).
- Si la posición está fuera de rango (menor a 1 o mayor al total) → muestra error y no guarda.
- Si la posición es válida → elimina la tarea.
- No se pide confirmación.
- Tras eliminar, las posiciones se reordenan automáticamente.

### Menú interactivo
```
=== GESTOR DE TAREAS ===
1. Agregar tarea
2. Listar tareas
3. Eliminar tarea
4. Salir

Selecciona una opción: _
```
- Opción inválida → muestra error y vuelve al menú.
- Opción 4 (Salir) → termina el programa.

### Validaciones en `main()`
- Título vacío al agregar.
- Posición no numérica al eliminar.
- Posición fuera de rango al eliminar.

### Formato del archivo `todos.csv`
```csv
titulo
Comprar leche
Estudiar Python
Llamar al cliente
```
Una sola columna `titulo` con cabecera. Sin comillas ni escapes especiales.

## Lo que NO incluye
- Edición de tareas
- Confirmación al eliminar
- Colores en la terminal
- Múltiples listas
- Fechas, IDs únicos ni metadatos adicionales
