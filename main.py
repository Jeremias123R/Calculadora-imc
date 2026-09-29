from database import conectar_db

def calcular_imc(peso, altura):
return peso / (altura ** 2)

def clasificar_imc(imc):
if imc < 18.5:
return "Bajo peso"
elif imc < 25:
return "Peso normal"
elif imc < 30:
return "Sobrepeso"
else:
return "Obesidad"

def mostrar_persona(registro):
print("\n----------------------------")
print("ID:", registro[0])
print("Nombre:", registro[1])
print("Edad:", registro[2], "años")
print("Peso:", registro[3], "kg")
print("Altura:", registro[4], "m")
print("IMC:", registro[5])
print("Categoría:", registro[6])
print("----------------------------")

def registrar_persona():
print("\n=== REGISTRAR PERSONA ===")

while True:
    nombre = input("¿Cuál es tu nombre? ")

    if nombre.replace(" ", "").isalpha():
        break

    print("Error: el nombre solo debe contener letras.")

while True:
    try:
        edad = int(input("¿Cuál es tu edad? "))

        if edad <= 0:
            print("Error: la edad debe ser mayor que 0.")
            continue

        break

    except ValueError:
        print("Error: debes introducir una edad válida.")

while True:
    try:
        peso = float(input("¿Cuál es tu peso en kg? "))
        altura = float(input("¿Cuál es tu altura en metros? "))

        if peso <= 0 or altura <= 0:
            print("Error: el peso y la altura deben ser mayores que 0.")
            continue

        break

    except ValueError:
        print("Error: debes introducir números.")

imc = calcular_imc(peso, altura)
categoria = clasificar_imc(imc)

conexion = conectar_db()
cursor = conexion.cursor()

cursor.execute("""
    INSERT INTO personas
    (nombre, edad, peso, altura, imc, categoria)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    nombre,
    edad,
    peso,
    altura,
    round(imc, 2),
    categoria
))

conexion.commit()
conexion.close()

print("\nPersona registrada correctamente.")
print(nombre + ", tu IMC es:", round(imc, 2))
print("Categoría:", categoria)

def ver_historial():
print("\n=== HISTORIAL ===")

conexion = conectar_db()
cursor = conexion.cursor()

cursor.execute("""
    SELECT id, nombre, edad, peso, altura, imc, categoria
    FROM personas
""")

personas = cursor.fetchall()
conexion.close()

if not personas:
    print("No hay personas registradas.")
    return

for persona in personas:
    mostrar_persona(persona)

def buscar_persona():
print("\n=== BUSCAR PERSONA ===")

nombre_buscar = input("Ingrese el nombre a buscar: ")

conexion = conectar_db()
cursor = conexion.cursor()

cursor.execute("""
    SELECT id, nombre, edad, peso, altura, imc, categoria
    FROM personas
    WHERE nombre LIKE ?
""", ("%" + nombre_buscar + "%",))

personas = cursor.fetchall()
conexion.close()

if not personas:
    print("No se encontró ninguna persona con ese nombre.")
    return

for persona in personas:
    mostrar_persona(persona)

def editar_persona():
print("\n=== EDITAR PERSONA ===")

nombre_buscar = input("Ingrese el nombre de la persona: ")

conexion = conectar_db()
cursor = conexion.cursor()

cursor.execute("""
    SELECT id, nombre, edad, peso, altura, imc, categoria
    FROM personas
    WHERE nombre LIKE ?
""", ("%" + nombre_buscar + "%",))

personas = cursor.fetchall()

if not personas:
    print("No se encontró ninguna persona.")
    conexion.close()
    return

for persona in personas:
    mostrar_persona(persona)

while True:
    try:
        id_editar = int(input("\nIngrese el ID que desea editar: "))
        break
    except ValueError:
        print("Error: introduzca un ID válido.")

while True:
    try:
        nuevo_peso = float(input("Nuevo peso en kg: "))
        nueva_altura = float(input("Nueva altura en metros: "))

        if nuevo_peso <= 0 or nueva_altura <= 0:
            print("Error: los valores deben ser mayores que 0.")
            continue

        break

    except ValueError:
        print("Error: debes introducir números.")

nuevo_imc = calcular_imc(nuevo_peso, nueva_altura)
nueva_categoria = clasificar_imc(nuevo_imc)

cursor.execute("""
    UPDATE personas
    SET peso = ?,
        altura = ?,
        imc = ?,
        categoria = ?
    WHERE id = ?
""", (
    nuevo_peso,
    nueva_altura,
    round(nuevo_imc, 2),
    nueva_categoria,
    id_editar
))

conexion.commit()
conexion.close()

print("\nPersona actualizada correctamente.")
print("Nuevo IMC:", round(nuevo_imc, 2))
print("Nueva categoría:", nueva_categoria)

def eliminar_persona():
print("\n=== ELIMINAR PERSONA ===")

nombre_buscar = input("Ingrese el nombre de la persona: ")

conexion = conectar_db()
cursor = conexion.cursor()

cursor.execute("""
    SELECT id, nombre, edad, peso, altura, imc, categoria
    FROM personas
    WHERE nombre LIKE ?
""", ("%" + nombre_buscar + "%",))

personas = cursor.fetchall()

if not personas:
    print("No se encontró ninguna persona.")
    conexion.close()
    return

for persona in personas:
    mostrar_persona(persona)

while True:
    try:
        id_eliminar = int(input("\nIngrese el ID que desea eliminar: "))
        break
    except ValueError:
        print("Error: introduzca un ID válido.")

confirmacion = input(
    "¿Está seguro de eliminar este registro? (s/n): "
).lower()

if confirmacion == "s":
    cursor.execute("""
        DELETE FROM personas
        WHERE id = ?
    """, (id_eliminar,))

    conexion.commit()
    print("Persona eliminada correctamente.")
else:
    print("Operación cancelada.")

conexion.close()

def mostrar_estadisticas():
print("\n=== ESTADÍSTICAS ===")

conexion = conectar_db()
cursor = conexion.cursor()

cursor.execute("SELECT COUNT(*) FROM personas")
total = cursor.fetchone()[0]

cursor.execute("SELECT AVG(imc) FROM personas")
promedio = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*)
    FROM personas
    WHERE categoria = 'Bajo peso'
""")
bajo_peso = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*)
    FROM personas
    WHERE categoria = 'Peso normal'
""")
peso_normal = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*)
    FROM personas
    WHERE categoria = 'Sobrepeso'
""")
sobrepeso = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*)
    FROM personas
    WHERE categoria = 'Obesidad'
""")
obesidad = cursor.fetchone()[0]

conexion.close()

print("Total de personas:", total)

if promedio is not None:
    print("IMC promedio:", round(promedio, 2))
else:
    print("IMC promedio: No hay datos.")

print("Bajo peso:", bajo_peso)
print("Peso normal:", peso_normal)
print("Sobrepeso:", sobrepeso)
print("Obesidad:", obesidad)

def mostrar_menu():
print("\n================================")
print("       CALCULADORA DE IMC")
print("================================")
print("1. Registrar persona")
print("2. Ver historial")
print("3. Buscar persona")
print("4. Editar persona")
print("5. Eliminar persona")
print("6. Ver estadísticas")
print("7. Salir")

conexion = conectar_db()
print("Base de datos conectada correctamente.")
conexion.close()

while True:

mostrar_menu()

opcion = input("Seleccione una opción: ")

if opcion == "1":
    registrar_persona()

elif opcion == "2":
    ver_historial()

elif opcion == "3":
    buscar_persona()

elif opcion == "4":
    editar_persona()

elif opcion == "5":
    eliminar_persona()

elif opcion == "6":
    mostrar_estadisticas()

elif opcion == "7":
    print("Programa finalizado.")
    break

else:
    print("Opción no válida.")
