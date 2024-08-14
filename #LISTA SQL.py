import sqlite3

def conexion_db():
    return sqlite3.connect("tareas.db")

def crear_tabla(lista):
    conexion = conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {lista} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarea TEXT NOT NULL,
        completada BOOLEAN NOT NULL
    )
    ''')
    
    conexion.commit()
    conexion.close()

def crear_lista():
    nombre_lista = input("Introduce el nombre de la nueva lista: ")
    crear_tabla(nombre_lista)
    print(f"Lista '{nombre_lista}' creada exitosamente.")

def agregar_tarea():
    lista_seleccionada = input("Selecciona la lista a la que quieras agregar una tarea (o introduce el nombre de una nueva lista): ")
    
    # Verificar y crear la tabla si no existe
    crear_tabla(lista_seleccionada)
    
    tarea = input("Introduce la tarea: ")
    
    conexion = conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute(f'''
    INSERT INTO {lista_seleccionada} (tarea, completada)
    VALUES (?, ?)
    ''', (tarea, False))
    
    conexion.commit()
    conexion.close()
    
    print(f"Tarea '{tarea}' agregada a {lista_seleccionada}.")

def marcar_completada():
    lista_seleccionada = input("Selecciona la lista de la cual marcar una tarea como completada: ")
    
    # Verificar y crear la tabla si no existe
    crear_tabla(lista_seleccionada)
    
    conexion = conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute(f'SELECT id, tarea FROM {lista_seleccionada} WHERE completada = ?', (False,))
    tareas = cursor.fetchall()
    
    if tareas:
        print(f"\nTareas en {lista_seleccionada}:")
        for i, (id, tarea) in enumerate(tareas):
            print(f"{i + 1}. {tarea}")
        
        index = int(input("Introduce el número de la tarea que quieres marcar como completada: ")) - 1
        if 0 <= index < len(tareas):
            id_tarea = tareas[index][0]
            cursor.execute(f'UPDATE {lista_seleccionada} SET completada = ? WHERE id = ?', (True, id_tarea))
            conexion.commit()
            print(f"Tarea '{tareas[index][1]}' marcada como completada.")
        else:
            print("Número de tarea no válido.")
    else:
        print(f"La lista '{lista_seleccionada}' está vacía.")
    
    conexion.close()

def eliminar_tarea():
    lista_seleccionada = input("Selecciona la lista de la cual eliminar una tarea: ")
    
    # Verificar y crear la tabla si no existe
    crear_tabla(lista_seleccionada)
    
    conexion = conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute(f'SELECT id, tarea FROM {lista_seleccionada}')
    tareas = cursor.fetchall()
    
    if tareas:
        print(f"\nTareas en {lista_seleccionada}:")
        for i, (id, tarea) in enumerate(tareas):
            print(f"{i + 1}. {tarea}")
        
        index = int(input("Introduce el número de la tarea que quieres eliminar: ")) - 1
        if 0 <= index < len(tareas):
            id_tarea = tareas[index][0]
            cursor.execute(f'DELETE FROM {lista_seleccionada} WHERE id = ?', (id_tarea,))
            conexion.commit()
            print(f"Tarea '{tareas[index][1]}' eliminada de {lista_seleccionada}.")
        else:
            print("Número de tarea no válido.")
    else:
        print(f"La lista '{lista_seleccionada}' está vacía.")
    
    conexion.close()

def eliminar_lista():
    lista_seleccionada = input("Introduce el nombre de la lista que deseas eliminar: ")
    
    conexion = conexion_db()
    cursor = conexion.cursor()
    
    # Eliminar la tabla correspondiente a la lista
    try:
        cursor.execute(f'DROP TABLE IF EXISTS {lista_seleccionada}')
        conexion.commit()
        print(f"Lista '{lista_seleccionada}' eliminada exitosamente.")
    except sqlite3.OperationalError as e:
        print(f"Error al eliminar la lista '{lista_seleccionada}': {e}")
    
    conexion.close()

def mostrar_listas():
    conexion = conexion_db()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"')
    listas = cursor.fetchall()
    
    for lista in listas:
        lista_nombre = lista[0]
        cursor.execute(f'SELECT tarea FROM {lista_nombre}')
        tareas = cursor.fetchall()
        print(f"\n{lista_nombre}:")
        for tarea in tareas:
            print(f"- {tarea[0]}")
    
    conexion.close()

def mostrar_menu():
    print("\nOpciones:")
    print("1. Crear nueva lista")
    print("2. Agregar tarea")
    print("3. Marcar tarea como completada")
    print("4. Eliminar tarea")
    print("5. Mostrar listas")
    print("6. Eliminar lista")
    print("7. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-7): ")
        if opcion == "1":
            crear_lista()
        elif opcion == "2":
            agregar_tarea()
        elif opcion == "3":
            marcar_completada()
        elif opcion == "4":
            eliminar_tarea()
        elif opcion == "5":
            mostrar_listas()
        elif opcion == "6":
            eliminar_lista()
        elif opcion == "7":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, elige una opción del menú.")

if __name__ == "__main__":
    main()
