import sqlite3
import tkinter as tk
from tkinter import messagebox

# Función para consultar la base de datos y filtrar Pokémon
def obtener_recomendaciones(tipo_enemigo, tipo_preferencia, nivel_preferencia, velocidad_preferencia):
    conn = sqlite3.connect('pokemon_battle.db')
    cursor = conn.cursor()

    # Paso 1: Consultar tipos fuertes contra el tipo enemigo
    cursor.execute("SELECT tipo_fuerte FROM relaciones WHERE tipo_debil = ?", (tipo_enemigo,))
    tipos_fuertes = [row[0] for row in cursor.fetchall()]

    # Paso 2: Filtrar Pokémon por tipo fuerte y demás preferencias
    cursor.execute("""
        SELECT nombre, tipo, tipo_ataque, nivel, velocidad 
        FROM pokemons 
        WHERE tipo IN ({})""".format(",".join("?" * len(tipos_fuertes))),
        tipos_fuertes)

    pokemons = cursor.fetchall()
    conn.close()

    # Paso 3: Calcular puntuaciones
    puntuaciones = []
    for nombre, tipo, tipo_ataque, nivel, velocidad in pokemons:
        puntos = 0
        if tipo in tipos_fuertes:
            puntos += 3
        if tipo_ataque == tipo_preferencia:
            puntos += 2
        if nivel_preferencia == "bajo" and nivel < 40 or \
           nivel_preferencia == "medio" and 40 <= nivel <= 60 or \
           nivel_preferencia == "alto" and nivel > 60:
            puntos += 2
        if velocidad == velocidad_preferencia:
            puntos += 1
        puntuaciones.append((nombre, tipo, puntos))

    # Ordenar Pokémon por puntuación
    puntuaciones.sort(key=lambda x: x[2], reverse=True)
    return puntuaciones[:3]

# Función para mostrar las recomendaciones
def mostrar_recomendaciones():
    tipo_enemigo = tipo_enemigo_var.get().lower()
    tipo_preferencia = tipo_preferencia_var.get().lower()
    nivel_preferencia = nivel_preferencia_var.get().lower()
    velocidad_preferencia = velocidad_preferencia_var.get().lower()

    if not all([tipo_enemigo, tipo_preferencia, nivel_preferencia, velocidad_preferencia]):
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
        return

    recomendaciones = obtener_recomendaciones(tipo_enemigo, tipo_preferencia, nivel_preferencia, velocidad_preferencia)
    if not recomendaciones:
        messagebox.showinfo("Recomendaciones", "No se encontraron Pokémon adecuados.")
    else:
        # Mostrar solo la primera recomendación para evitar repetir resultados
        nombre, tipo, _ = recomendaciones[0]
        messagebox.showinfo("Recomendación", f"El Pokémon recomendado es {nombre} ({tipo}).")

# Interfaz gráfica
root = tk.Tk()
root.title("Sistema Experto Pokémon")
root.geometry("500x500")
root.config(bg="#6A5ACD")  # Color de fondo morado

# Preguntas y entradas con colores morados
tk.Label(root, text="Tipo de Pokémon enemigo (fuego, agua, etc.):", bg="#6A5ACD", fg="white", font=("Arial", 12)).pack(pady=5)
tipo_enemigo_var = tk.StringVar()
tk.Entry(root, textvariable=tipo_enemigo_var, bg="white", font=("Arial", 10)).pack(pady=5)

tk.Label(root, text="Preferencia de tipo de ataque (físico/especial):", bg="#6A5ACD", fg="white", font=("Arial", 12)).pack(pady=5)
tipo_preferencia_var = tk.StringVar()
tk.Entry(root, textvariable=tipo_preferencia_var, bg="white", font=("Arial", 10)).pack(pady=5)

tk.Label(root, text="Nivel preferido (bajo/medio/alto):", bg="#6A5ACD", fg="white", font=("Arial", 12)).pack(pady=5)
nivel_preferencia_var = tk.StringVar()
tk.Entry(root, textvariable=nivel_preferencia_var, bg="white", font=("Arial", 10)).pack(pady=5)

tk.Label(root, text="Velocidad preferida (alta/media/baja):", bg="#6A5ACD", fg="white", font=("Arial", 12)).pack(pady=5)
velocidad_preferencia_var = tk.StringVar()
tk.Entry(root, textvariable=velocidad_preferencia_var, bg="white", font=("Arial", 10)).pack(pady=5)

# Botón para obtener recomendaciones con colores morados
tk.Button(root, text="Obtener Recomendaciones", command=mostrar_recomendaciones, bg="#8A2BE2", fg="white", font=("Arial", 12)).pack(pady=20)

# Iniciar la interfaz
root.mainloop()