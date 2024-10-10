import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox

# Función para cargar el XML y extraer las preguntas
def cargar_preguntas_desde_xml(ruta_xml):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()
    preguntas = []

    for question in root.findall('question'):
        texto_pregunta = question.find('text').text
        opciones = [opt.text.strip() for opt in question.find('options').findall('option')]
        respuesta_correcta = question.find('answer').text.strip()  # Asumimos que la respuesta correcta está en formato "A", "B", "C", "D"
        preguntas.append({
            'texto': texto_pregunta,
            'opciones': opciones,
            'respuesta': respuesta_correcta
        })
    return preguntas

# Función que muestra la siguiente pregunta o el resultado final
def mostrar_pregunta():
    global pregunta_actual

    # Limpiar la ventana actual
    for widget in root.winfo_children():
        widget.destroy()

    if pregunta_actual < len(preguntas):
        # Mostrar la pregunta actual
        pregunta = preguntas[pregunta_actual]
        label_pregunta = tk.Label(root, text=f"Pregunta {pregunta_actual + 1}: {pregunta['texto']}", font=('Arial', 16), wraplength=500)
        label_pregunta.pack(pady=20)

        # Crear botones para cada opción
        for i, opcion_texto in enumerate(pregunta['opciones']):
            letra_opcion = chr(65 + i)  # Generar letras A, B, C, D
            boton_opcion = tk.Button(root, text=f"{letra_opcion}) {opcion_texto}",
                                     command=lambda opt=letra_opcion: validar_respuesta(opt),
                                     font=('Arial', 14),  # Aumentar el tamaño de la fuente
                                     bg="#4CAF50", fg="white", width=50, height=3, relief="raised", wraplength=400)
            boton_opcion.pack(pady=10)

    else:
        # Mostrar el resultado final
        messagebox.showinfo("Examen terminado", f"Tu puntuación es {puntaje} de {len(preguntas)}")
        root.quit()

# Función para validar la respuesta seleccionada
def validar_respuesta(respuesta):
    global puntaje, pregunta_actual

    # Obtener la respuesta correcta de la pregunta actual
    respuesta_correcta = preguntas[pregunta_actual]['respuesta']

    # Comparar la respuesta seleccionada con la correcta
    if respuesta == respuesta_correcta:
        puntaje += 1
        messagebox.showinfo("Correcto", "¡Respuesta correcta!")
    else:
        messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. La correcta era: {respuesta_correcta}")

    # Avanzar a la siguiente pregunta
    pregunta_actual += 1
    mostrar_pregunta()

# Cargar las preguntas desde el archivo XML
ruta_xml = "ruta.xml"  # Asegúrate de que la ruta al archivo sea correcta
preguntas = cargar_preguntas_desde_xml(ruta_xml)

# Variables globales
puntaje = 0
pregunta_actual = 0

# Crear la ventana de la aplicación
root = tk.Tk()
root.title("Examen Interactivo")
root.geometry("800x600")  # Aumentar el tamaño de la ventana

# Mostrar la primera pregunta
mostrar_pregunta()

# Iniciar la aplicación
root.mainloop()
