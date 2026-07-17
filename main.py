TODO_LIST = []


def load_todos():
    """Carga las tareas desde todos.csv. Si no existe, devuelve lista vacia."""
    import os

    if not os.path.exists("todos.csv"):
        return []

    tasks = []
    with open("todos.csv", "r") as f:
        lines = f.readlines()

    # Ignoramos la primera linea (cabecera)
    for line in lines[1:]:
        line = line.strip()
        if line:
            tasks.append(line)

    return tasks


def save_todos():
    """Guarda TODO_LIST en todos.csv con cabecera 'titulo'."""
    with open("todos.csv", "w") as f:
        f.write("titulo\n")
        for task in TODO_LIST:
            f.write(task + "\n")


def add_one_task(title):
    """Agrega una tarea a TODO_LIST si el titulo no esta vacio. Luego guarda."""
    if not title.strip():
        print("Error: El titulo no puede estar vacio.")
        return

    TODO_LIST.append(title)
    save_todos()
    print(f"Tarea '{title}' agregada correctamente.")


def delete_task(number_to_delete):
    """Elimina la tarea en la posicion number_to_delete (1-indexed). Luego guarda."""
    if number_to_delete < 1 or number_to_delete > len(TODO_LIST):
        print(f"Error: La posicion {number_to_delete} no es valida.")
        return

    removed = TODO_LIST.pop(number_to_delete - 1)
    save_todos()
    print(f"Tarea '{removed}' eliminada correctamente.")


def print_list():
    """Imprime las tareas de TODO_LIST numeradas desde 1."""
    if not TODO_LIST:
        print("No hay tareas pendientes.")
        return

    for i, task in enumerate(TODO_LIST):
        print(f"{i + 1}. {task}")


def show_menu():
    """Muestra el menu de opciones."""
    print("\n=== GESTOR DE TAREAS ===")
    print("1. Agregar tarea")
    print("2. Listar tareas")
    print("3. Eliminar tarea")
    print("4. Salir")


def main():
    """Bucle principal del programa."""
    global TODO_LIST
    TODO_LIST = load_todos()

    while True:
        show_menu()
        opcion = input("\nSelecciona una opcion: ").strip()

        if opcion == "1":
            titulo = input("Ingresa el titulo de la tarea: ").strip()
            add_one_task(titulo)

        elif opcion == "2":
            print_list()

        elif opcion == "3":
            try:
                num = int(input("Ingresa el numero de la tarea a eliminar: ").strip())
                delete_task(num)
            except ValueError:
                print("Error: Debes ingresar un numero valido.")

        elif opcion == "4":
            print("¡Hasta luego!")
            break

        else:
            print("Error: Opcion no valida. Intenta de nuevo.")


if __name__ == "__main__":
    main()