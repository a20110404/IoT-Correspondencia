import os
import json
import subprocess
import sys

RUTA_JSON = "out/personas_aleatorias.json"

def cargar_personas():
    if not os.path.exists(RUTA_JSON):
        return []
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except Exception:
        return []

def obtener_columnas():
    personas = cargar_personas()
    if personas:
        return list(personas[0].keys())
    return []

def actualizar_tabla(tabla, columnas):
    for row in tabla.get_children():
        tabla.delete(row)
    personas = cargar_personas()
    for persona in personas:
        valores = [persona.get(col, "") for col in columnas]
        tabla.insert("", "end", values=valores)

def generar_personas(entry_num_personas, tabla, columnas, messagebox):
    try:
        n = int(entry_num_personas.get())
        if n <= 0:
            raise ValueError("El número debe ser mayor que cero.")
        subprocess.run(["python", "src/generar_personas.py"], input=str(n).encode())
        messagebox.showinfo("Éxito", f"Se generaron {n} personas.")
        # Actualizar columnas y tabla después de generar
        columnas[:] = obtener_columnas()
        tabla["columns"] = columnas
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=100)
        actualizar_tabla(tabla, columnas)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "Ocurrió un error al generar las personas.")

def guardar_cambios(tabla, columnas, messagebox):
    personas = []
    for row_id in tabla.get_children():
        valores = tabla.item(row_id)["values"]
        persona = {col: valores[i] for i, col in enumerate(columnas)}
        personas.append(persona)
    try:
        with open(RUTA_JSON, "w", encoding="utf-8") as f:
            json.dump(personas, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}")

def editar_celda(event, tabla, columnas, cargar_personas, messagebox):
    item = tabla.identify_row(event.y)
    columna = tabla.identify_column(event.x)
    if not item or not columna:
        return
    col_index = int(columna.replace('#', '')) - 1
    x, y, width, height = tabla.bbox(item, columna)
    valor_actual = tabla.item(item, "values")[col_index]

    from tkinter import Entry  # Importar aquí para evitar dependencias circulares
    entry_edit = Entry(tabla)
    entry_edit.place(x=x, y=y, width=width, height=height)
    entry_edit.insert(0, valor_actual)
    entry_edit.focus()

    def guardar_edicion(event=None):
        nuevo_valor = entry_edit.get()
        valores = list(tabla.item(item, "values"))
        valores[col_index] = nuevo_valor
        tabla.item(item, values=valores)
        entry_edit.destroy()
        try:
            personas = cargar_personas()
            id_editado = valores[0]
            for persona in personas:
                if str(persona.get("id")) == str(id_editado):
                    persona[columnas[col_index]] = nuevo_valor
                    break
            with open(RUTA_JSON, "w", encoding="utf-8") as f:
                json.dump(personas, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")

    entry_edit.bind("<Return>", guardar_edicion)
    entry_edit.bind("<FocusOut>", lambda e: entry_edit.destroy())

def abrir_plantilla():
    ruta = os.path.abspath("src/oficio_plantilla.txt")
    os.startfile(ruta)

def generar_oficios(messagebox, actualizar_tabla_oficios):
    try:
        subprocess.run([sys.executable, "src/Actividad4.py"], check=True)
        messagebox.showinfo("Éxito", "Oficios generados correctamente.")
        actualizar_tabla_oficios()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron generar los oficios: {e}")

def eliminar_persona(tabla, cargar_personas, messagebox, columnas, actualizar_tabla):
    item = tabla.selection()
    if not item:
        return
    valores = tabla.item(item, "values")
    if not valores:
        return
    id_eliminar = valores[0]
    respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar a la persona con id {id_eliminar}?")
    if not respuesta:
        return
    personas = cargar_personas()
    personas = [p for p in personas if str(p.get("id")) != str(id_eliminar)]
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(personas, f, ensure_ascii=False, indent=4)
    actualizar_tabla(tabla, columnas)
    messagebox.showinfo("Eliminado", f"Persona con id {id_eliminar} eliminada.")

def buscar_personas(entry_busqueda, tabla, columnas, cargar_personas):
    texto = entry_busqueda.get().strip().lower()
    for row in tabla.get_children():
        tabla.delete(row)
    personas = cargar_personas()
    for persona in personas:
        nombre = str(persona.get("nombre", "")).lower()
        apellido1 = str(persona.get("apellido1", "")).lower()
        apellido2 = str(persona.get("apellido2", "")).lower()
        if not texto or texto in nombre or texto in apellido1 or texto in apellido2:
            valores = [persona.get(col, "") for col in columnas]
            tabla.insert("", "end", values=valores)

def actualizar_tabla_oficios(tabla_oficios):
    for row in tabla_oficios.get_children():
        tabla_oficios.delete(row)
    carpeta = "oficios"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".pdf")]
    for archivo in archivos:
        tabla_oficios.insert("", "end", values=(archivo,))

def abrir_oficio(event, tabla_oficios, messagebox):
    item = tabla_oficios.identify_row(event.y)
    if not item:
        return
    archivo = tabla_oficios.item(item, "values")[0]
    ruta = os.path.abspath(os.path.join("oficios", archivo))
    try:
        os.startfile(ruta)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")