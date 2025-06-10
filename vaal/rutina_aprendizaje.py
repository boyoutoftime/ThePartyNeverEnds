import time
import os
import subprocess
import json
import re
import unicodedata
from lector import extraer_texto_de_pdf
from analizador import preprocesar
from normalizador import cargar_terminos, normalizar_palabra, guardar_diccionario

terminos = cargar_terminos()

# --- Gestión de símbolos ---
def cargar_simbolos(ruta='simbolos_aprendidos.json'):
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_simbolos(diccionario, ruta='simbolos_aprendidos.json'):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, indent=2, ensure_ascii=False)

def es_simbolo_valido(s):
    if not s or not s.isprintable() or s.isspace():
        return False
    categoria = unicodedata.category(s)
    return categoria in ('Sm', 'So', 'Sc')

def es_ecuacion(linea):
    if "=" in linea or re.search(r"\b\d+(\.\d+)?\b", linea):
        simbolos = re.findall(r"[^\w\s]", linea)
        simbolos_validos = [s for s in simbolos if es_simbolo_valido(s)]
        return len(simbolos_validos) / max(1, len(linea)) > 0.05
    return False

def extraer_simbolos(ecuacion):
    simbolos = set(re.findall(r"[^\w\s]", ecuacion))
    return sorted([s for s in simbolos if es_simbolo_valido(s)])

def es_pdf_ruidoso(texto):
    lineas = texto.split('\n')
    lineas_raras = [l for l in lineas if sum(1 for c in l if not c.isprintable()) > 5]
    return len(lineas_raras) > 20

# --- Análisis del PDF ---
def estudiar_pdf(ruta_pdf):
    print(f"\n📖 Estudiando: {ruta_pdf}")
    texto = extraer_texto_de_pdf(ruta_pdf)

    if es_pdf_ruidoso(texto):
        print(f"⚠️ PDF ignorado por contener texto no válido o binario: {ruta_pdf}")
        return

    # 🔍 Extraer y guardar símbolos de ecuaciones
    simbolos_aprendidos = cargar_simbolos()
    for linea in texto.split('\n'):
        if es_ecuacion(linea):
            nuevos = extraer_simbolos(linea)
            for s in nuevos:
                if s not in simbolos_aprendidos:
                    categoria = unicodedata.category(s)
                    simbolos_aprendidos[s] = f"Símbolo detectado en ecuación (Categoría Unicode: {categoria})"
                    print(f"➕ Símbolo nuevo: {s} ({categoria})")
    guardar_simbolos(simbolos_aprendidos)

    # 📚 Estudiar palabras del texto
    palabras = preprocesar(texto, terminos)
    for palabra in palabras:
        normalizar_palabra(palabra, terminos)

    time.sleep(2)

def descargar_articulos():
    print("🚀 Iniciando descarga de artículos con vaalinvestiga.py...")
    subprocess.run(["python", "vaalinvestiga.py"], check=True)
    print("✅ Descarga finalizada.\n")

def estudiar_todos_los_pdfs():
    carpeta = "pdfs"
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".pdf")]
    if not archivos:
        print("⚠️ No hay PDFs para estudiar.")
        return

    for archivo in archivos:
        ruta = os.path.join(carpeta, archivo)
        estudiar_pdf(ruta)
        try:
            os.remove(ruta)
            print(f"🗑️ Eliminado: {ruta}")
        except Exception as e:
            print(f"❌ Error al eliminar {ruta}: {e}")
        time.sleep(5)

# --- Flujo principal ---
if __name__ == '__main__':
    descargar_articulos()
    estudiar_todos_los_pdfs()
    guardar_diccionario(terminos)
    print("✅ Rutina completa. Conocimiento actualizado.")