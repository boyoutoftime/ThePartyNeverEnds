import time
import os
import subprocess
from lector import extraer_texto_de_pdf
from analizador import preprocesar
from normalizador import cargar_terminos, normalizar_palabra, guardar_diccionario

terminos = cargar_terminos()

def descargar_articulos():
    print("🚀 Iniciando descarga de artículos con vaalinvestiga.py...")
    subprocess.run(["python", "vaalinvestiga.py"], check=True)
    print("✅ Descarga finalizada.\n")

def estudiar_pdf(ruta_pdf):
    print(f"\n📖 Estudiando: {ruta_pdf}")
    texto = extraer_texto_de_pdf(ruta_pdf)
    palabras = preprocesar(texto, terminos)
    for palabra in palabras:
        normalizar_palabra(palabra, terminos)
    time.sleep(2)  # simula pausa entre lecturas

def estudiar_todos_los_pdfs():
    carpeta = "pdfs"
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".pdf")]
    if not archivos:
        print("⚠️ No hay PDFs para estudiar.")
        return

    for archivo in archivos:
        ruta = os.path.join(carpeta, archivo)
        estudiar_pdf(ruta)

        # ✅ Eliminar el PDF después de analizarlo
        try:
            os.remove(ruta)
            print(f"🗑️ Eliminado: {ruta}")
        except Exception as e:
            print(f"❌ Error al eliminar {ruta}: {e}")

        time.sleep(5)  # descanso entre artículos

if __name__ == '__main__':
    descargar_articulos()
    estudiar_todos_los_pdfs()
    guardar_diccionario(terminos)
    print("✅ Rutina completa. Conocimiento actualizado.")