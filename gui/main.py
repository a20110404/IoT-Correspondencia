from tkinter import Tk, Label, Entry, Button, messagebox, Frame, BOTH, END, Menu
from tkinter import ttk
import os
import sys

# Importa todas las funciones de lógica
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import logica as logic

# Configuración de la ventana principal
ventana = Tk()
ventana.title("Generador de Personas")
ventana.geometry("1200x650")

# Crear el notebook (pestañas)
notebook = ttk.Notebook(ventana)
notebook.pack(fill=BOTH, expand=True)

# Frame para la pestaña de personas
frame_personas = Frame(notebook)
notebook.add(frame_personas, text="Personas")

# Frame para la pestaña de oficios
frame_oficios = Frame(notebook)
notebook.add(frame_oficios, text="Oficios generados")

# Widgets de personas
label_num_personas = Label(frame_personas, text="Número de personas a generar:")
label_num_personas.pack(pady=10)

entry_num_personas = Entry(frame_personas)
entry_num_personas.pack(pady=5)

# Boton personalizado
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton",
    font=("Segoe UI", 11, "bold"),
    foreground="#ffffff",
    background="#0078D7",
    padding=6,
    borderwidth=2)
style.map("TButton",
    background=[('active', '#005A9E')],
    foreground=[('active', '#ffffff')])

# Botón para generar personas
boton_generar = ttk.Button(
    frame_personas, text="Generar",
    command=lambda: logic.generar_personas(entry_num_personas, tabla, columnas, messagebox),
    style="TButton"
)
boton_generar.pack(pady=10)

# Campo y botón de búsqueda
frame_busqueda = Frame(frame_personas)
frame_busqueda.pack(pady=5)

label_busqueda = Label(frame_busqueda, text="Buscar por nombre o apellidos:")
label_busqueda.pack(side="left", padx=5)

entry_busqueda = Entry(frame_busqueda)
entry_busqueda.pack(side="left", padx=5)

boton_buscar = ttk.Button(
    frame_busqueda, text="Buscar",
    command=lambda: logic.buscar_personas(entry_busqueda, tabla, columnas, logic.cargar_personas),
    style="TButton"
)
boton_buscar.pack(side="left", padx=5)

# Tabla para mostrar personas
frame_tabla = Frame(frame_personas)
frame_tabla.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Obtener columnas dinámicamente
columnas = logic.obtener_columnas()
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=100)
tabla.pack(fill=BOTH, expand=True)

tabla.bind(
    "<Double-1>",
    lambda event: logic.editar_celda(event, tabla, columnas, logic.cargar_personas, messagebox)
)

# Crear menú contextual
menu_persona = Menu(tabla, tearoff=0)
menu_persona.add_command(
    label="Eliminar",
    command=lambda: logic.eliminar_persona(tabla, logic.cargar_personas, messagebox, columnas, lambda t, c: logic.actualizar_tabla(t, c))
)

def mostrar_menu_persona(event):
    item = tabla.identify_row(event.y)
    if item:
        tabla.selection_set(item)
        menu_persona.tk_popup(event.x_root, event.y_root)

tabla.bind("<Button-3>", mostrar_menu_persona)

logic.actualizar_tabla(tabla, columnas)

# Botón para guardar cambios
boton_guardar = ttk.Button(
    frame_personas, text="Guardar cambios",
    command=lambda: logic.guardar_cambios(tabla, columnas, messagebox),
    style="TButton"
)
boton_guardar.pack(pady=5)

# Botón para abrir la plantilla de oficio
boton_abrir_plantilla = ttk.Button(
    frame_personas, text="Abrir plantilla de oficio",
    command=logic.abrir_plantilla,
    style="TButton"
)
boton_abrir_plantilla.pack(pady=5)

# --- Tabla de archivos PDF en la pestaña de oficios ---
def actualizar_tabla_oficios():
    logic.actualizar_tabla_oficios(tabla_oficios)

tabla_oficios = ttk.Treeview(frame_oficios, columns=("Archivo PDF",), show="headings")
tabla_oficios.heading("Archivo PDF", text="Archivo PDF")
tabla_oficios.column("Archivo PDF", width=600)
tabla_oficios.pack(fill=BOTH, expand=True, padx=10, pady=10)

tabla_oficios.bind(
    "<Double-1>",
    lambda event: logic.abrir_oficio(event, tabla_oficios, messagebox)
)

# Botón para generar oficios
boton_generar_oficios = ttk.Button(
    frame_personas, text="Generar oficios PDF",
    command=lambda: logic.generar_oficios(messagebox, actualizar_tabla_oficios),
    style="TButton"
)
boton_generar_oficios.pack(pady=5)

# Llama a la función para mostrar los archivos al iniciar
actualizar_tabla_oficios()

ventana.mainloop()