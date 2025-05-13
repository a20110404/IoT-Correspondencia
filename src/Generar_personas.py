import json
from faker import Faker
from datetime import datetime

fake = Faker('es_MX')  # Datos en español y estilo mexicano

def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()

    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def generar_persona(id_persona):
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=90)
    persona = {
        "id": id_persona,
        "nombre": fake.first_name(),
        "apellido1": fake.last_name(),
        "apellido2": fake.last_name(),
        "cargo": fake.job(),
        "empresa": fake.company(),
        "calle": fake.street_name(),
        "numeroExt": fake.building_number(),
        "numeroInt": str(fake.random_int(min=1, max=50)),
        "colonia": fake.city_suffix(),
        "municipio": fake.city(),
        "estado": fake.state(),
        "codigoPostal": fake.postcode(),
        "telefono": fake.phone_number(),
        "correoElectronico": fake.email(),
        "fechaNacimiento": fecha_nacimiento.strftime("%Y-%m-%d"),
        "edad": calcular_edad(fecha_nacimiento)
    }
    return persona

def main():
    personas = []
    n = int(input(""))

    for i in range(1, n + 1):
        personas.append(generar_persona(i))

    with open("out/personas_aleatorias.json", "w", encoding="utf-8") as archivo:
        json.dump(personas, archivo, indent=4, ensure_ascii=False)

    print(f"\nSe generaron {n} personas y se guardaron en 'personas_aleatorias.json'.")

if __name__ == "__main__":
    main()