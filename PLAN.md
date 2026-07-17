# PLAN.md — Plan de implementación

## Estado compartido
```python
TODO_LIST = []   # variable global, manipulada por todas las funciones
```

## Funciones del programa

| Función | Parámetros | Retorno | Descripción |
|---|---|---|---|
| `load_todos()` | — | `list[str]` | Lee `todos.csv`, ignora cabecera, devuelve lista de títulos. Si no existe, devuelve `[]`. |
| `save_todos()` | — | `None` | Escribe cabecera `titulo` y una línea por cada tarea desde `TODO_LIST`. |
| `add_one_task(title)` | `title: str` | `None` | Valida que `title` no esté vacío, lo agrega al final de `TODO_LIST` y llama a `save_todos()`. |
| `delete_task(number_to_delete)` | `number_to_delete: int` | `None` | Valida que `number_to_delete` esté en rango (1..len), elimina la tarea y llama a `save_todos()`. |
| `print_list()` | — | `None` | Imprime cada tarea como `{pos}. {titulo}` (desde 1). Si está vacía, muestra mensaje. |
| `show_menu()` | — | `None` | Imprime las opciones del menú interactivo. |
| `main()` | — | `None` | Bucle principal: `load_todos()`, menú, opciones, acciones. |

## Orden de implementación (6 pasos)

### Paso 1 — `load_todos()`
- Leer `todos.csv` línea por línea.
- Ignorar la primera línea (cabecera).
- Devolver `list[str]` con los títulos.
- Si el archivo no existe, devolver `[]`.
- **Comprobación:** Crear `todos.csv` manual con 2 tareas y probar. Probar también sin archivo.

### Paso 2 — `save_todos()`
- Abrir `todos.csv` en modo escritura.
- Escribir cabecera `titulo\n`.
- Escribir una línea por cada elemento de `TODO_LIST`.
- **Comprobación:** Llenar `TODO_LIST` manual, llamar `save_todos()`, abrir CSV y verificar.

### Paso 3 — `print_list()`
- Si `TODO_LIST` está vacía → imprimir mensaje de lista vacía.
- Si tiene elementos → imprimir `{i+1}. {TODO_LIST[i]}` para cada uno.
- **Comprobación:** Probar con lista vacía y con 3 tareas.

### Paso 4 — `add_one_task(title)`
- Si `title` está vacío → imprimir error y retornar.
- Si es válido → `TODO_LIST.append(title)` → `save_todos()`.
- **Comprobación:** Agregar tarea válida, listar, revisar CSV. Agregar título vacío → solo error, sin cambios.

### Paso 5 — `delete_task(number_to_delete)`
- Si `number_to_delete < 1` o `number_to_delete > len(TODO_LIST)` → imprimir error y retornar.
- Si es válido → `TODO_LIST.pop(number_to_delete - 1)` → `save_todos()`.
- **Comprobación:** Eliminar posición existente, listar, revisar CSV. Probar posición inválida.

### Paso 6 — `show_menu()` + `main()`
- `show_menu()` imprime el menú.
- `main()`:
  1. `TODO_LIST = load_todos()`
  2. Bucle infinito:
     - `show_menu()`
     - Pedir opción
     - Opción 1: pedir título → `add_one_task(title)`
     - Opción 2: `print_list()`
     - Opción 3: pedir número → validar entero → `delete_task(int(num))`
     - Opción 4: `break`
     - Otro: mostrar error
- **Comprobación:** `python main.py` y probar todo el flujo. Verificar persistencia entre ejecuciones.

## Notas de diseño
- `add_one_task` y `delete_task` reciben datos ya validados por `main()`.
- `main()` se encarga de toda la interacción con el usuario (inputs y validación de formato).
- `main.py` es el único archivo del programa.
