import json
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

def cargar_personas(archivo_json):
    with open(archivo_json, "r", encoding="utf-8") as f:
        return json.load(f)

def cargar_plantilla(archivo_plantilla):
    with open(archivo_plantilla, "r", encoding="utf-8") as f:
        return f.read()

def crear_oficio_pdf(persona):
    fecha_actual = datetime.today().strftime("%d/%m/%Y")
    # Crear la carpeta 'oficios' si no existe
    carpeta_oficios = "oficios"
    if not os.path.exists(carpeta_oficios):
        os.makedirs(carpeta_oficios)
    nombre_archivo = os.path.join(
        carpeta_oficios,
        f"oficio_{persona['nombre']}_{persona['apellido1']}.pdf"
    )

    # Leer la plantilla desde el archivo
    plantilla = cargar_plantilla("src/oficio_plantilla.txt")

    # Formatear la plantilla con los datos de la persona
    contenido = plantilla.format(
        fecha_actual=fecha_actual,
        nombre=persona['nombre'],
        apellido1=persona['apellido1'],
        apellido2=persona['apellido2'],
        cargo=persona['cargo'],
        empresa=persona['empresa'],
        calle=persona['calle'],
        numeroExt=persona['numeroExt'],
        numeroInt=persona['numeroInt'],
        colonia=persona['colonia'],
        municipio=persona['municipio'],
        estado=persona['estado'],
        codigoPostal=persona['codigoPostal'],
        telefono=persona['telefono'],
        correoElectronico=persona['correoElectronico'],
        fechaNacimiento=persona['fechaNacimiento'],
        edad=persona['edad']
    )

    # Crear un objeto canvas para el PDF
    c = canvas.Canvas(nombre_archivo, pagesize=LETTER)
    width, height = LETTER

    texto = c.beginText(50, height - 50)
    texto.setFont("Helvetica", 11)

    # Agregar el contenido formateado al PDF
    for linea in contenido.splitlines():
        texto.textLine(linea)

    c.drawText(texto)
    c.save()
    print(f"✅ PDF generado: {nombre_archivo}")

def main():
    personas = cargar_personas("out/personas_aleatorias.json")
    for persona in personas:
        crear_oficio_pdf(persona)

if __name__ == "__main__":
    main()