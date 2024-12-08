import sqlite3

# Conectamos a la base de datos (se crea si no existe)
conn = sqlite3.connect('pokemon_battle.db')
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
CREATE TABLE IF NOT EXISTS pokemons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    tipo_ataque TEXT NOT NULL,
    nivel INTEGER NOT NULL,
    velocidad TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS relaciones (
    tipo_debil TEXT NOT NULL,
    tipo_fuerte TEXT NOT NULL,
    PRIMARY KEY (tipo_debil, tipo_fuerte)
);
''')

# Insertar datos en pokemons
cursor.executemany('''
INSERT OR IGNORE INTO pokemons (nombre, tipo, tipo_ataque, nivel, velocidad) VALUES (?, ?, ?, ?, ?);
''', [
    ('Charizard', 'fuego', 'especial', 50, 'alta'),
    ('Blastoise', 'agua', 'especial', 52, 'media'),
    ('Pikachu', 'eléctrico', 'físico', 35, 'alta'),
    ('Venusaur', 'planta', 'especial', 53, 'baja'),
    ('Machamp', 'lucha', 'físico', 45, 'media'),
    ('Alakazam', 'psíquico', 'especial', 48, 'alta'),
    ('Gengar', 'fantasma', 'especial', 49, 'alta'),
    ('Snorlax', 'normal', 'físico', 42, 'baja'),
    ('Jolteon', 'eléctrico', 'físico', 39, 'alta'),  # Representante adicional de eléctrico
    ('Glaceon', 'hielo', 'especial', 47, 'media'),  # Representante adicional de hielo
    ('Umbreon', 'siniestro', 'especial', 50, 'baja'),  # Representante adicional de siniestro
    ('Steelix', 'acero', 'físico', 51, 'media'),  # Representante adicional de acero
    ('Sylveon', 'hada', 'especial', 47, 'baja'),  # Representante adicional de hada
    ('Pidgeot', 'volador', 'físico', 46, 'media'),  # Representante adicional de volador
    ('Groudon', 'tierra', 'físico', 54, 'baja'),  # Representante adicional de tierra
    ('Dragonite', 'dragón', 'especial', 50, 'alta'),  # Representante adicional de dragón
    ('Scyther', 'bicho', 'físico', 47, 'alta'),  # Representante adicional de bicho
    ('Weezing', 'veneno', 'especial', 40, 'media'),  # Representante adicional de veneno
])

# Insertar datos en relaciones
cursor.executemany('''
INSERT OR IGNORE INTO relaciones (tipo_debil, tipo_fuerte) VALUES (?, ?);
''', [
    ('fuego', 'agua'),
    ('agua', 'eléctrico'),
    ('planta', 'fuego'),
    ('eléctrico', 'tierra'),
    ('tierra', 'agua'),
    ('psíquico', 'fantasma'),
    ('lucha', 'psíquico'),
    ('fuego', 'roca'),
    ('hielo', 'fuego'),
    ('hielo', 'roca'),
    ('fantasma', 'normal'),
    ('siniestro', 'psíquico'),
    ('acero', 'fuego'),
    ('hada', 'dragón'),
    ('volador', 'eléctrico'),
    ('tierra', 'agua'),
    ('dragón', 'hielo'),
    ('bicho', 'volador'),
    ('veneno', 'psíquico'),
    ('normal', 'lucha'),
    ('agua', 'planta'),  # Relación de tipo para agua y planta
    ('eléctrico', 'agua'),  # Relación de tipo para eléctrico y agua
    ('roca', 'fuego'),  # Relación de tipo para roca y fuego
    ('roca', 'hielo'),  # Relación de tipo para roca y hielo
    ('siniestro', 'hielo'),  # Relación de tipo para siniestro y hielo
    ('físico', 'especial'),  # Representante adicional de siniestro
])

# Confirmar que los datos han sido insertados
conn.commit()

print("Base de datos actualizada correctamente con los datos proporcionados.")

# Cerrar la conexión
conn.close()