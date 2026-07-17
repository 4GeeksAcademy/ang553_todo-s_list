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
    """Stub"""
    pass


def delete_task(number_to_delete):
    """Stub"""
    pass


def print_list():
    """Stub"""
    pass


def show_menu():
    """Stub"""
    pass


def main():
    """Stub"""
    pass


if __name__ == "__main__":
    main()