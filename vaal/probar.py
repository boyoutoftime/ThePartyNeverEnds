import os
import json
import re
from lector import extraer_texto_de_pdf

# Ruta del PDF para prueba
PDF_PRUEBA = "pdfs/ejemplo_arxiv.pdf"  # Asegúrate de que exista

# Cargar o crear diccionario de símbolos aprendidos
def cargar_simbolos(ruta='simbolos_aprendidos.json'):
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_simbolos(diccionario, ruta='simbolos_aprendidos.json'):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, indent=2, ensure_ascii=False)

# Detecta si una línea parece una ecuación científica
def es_ecuacion(linea):
    if "=" in linea or re.search(r"\b\d+(\.\d+)?\b", linea):
        simbolos = re.findall(r"[^\w\s]", linea)  # signos no alfanuméricos
        if len(simbolos) / max(1, len(linea)) > 0.1:
            return True
    return False

# Extrae símbolos individuales usados en la ecuación
def extraer_simbolos(ecuacion):
    return sorted(set(re.findall(r"[^\w\s]", ecuacion)))

# --- Flujo principal ---
if __name__ == '__main__':
    if not os.path.exists(PDF_PRUEBA):
        print("❌ No se encontró el PDF de prueba.")
        exit()

    texto = extraer_texto_de_pdf(PDF_PRUEBA)
    lineas = texto.split('\n')
    simbolos_aprendidos = cargar_simbolos()

    for linea in lineas:
        if es_ecuacion(linea):
            print(f"\n🧮 Ecuación detectada:\n{linea.strip()}")
            nuevos = extraer_simbolos(linea)
            for s in nuevos:
                if s not in simbolos_aprendidos:
                    simbolos_aprendidos[s] = "Símbolo detectado en ecuación"
                    print(f"➕ Nuevo símbolo aprendido: {s}")

    guardar_simbolos(simbolos_aprendidos)
    print("\n✅ Lectura de ecuaciones completada. Simbolos guardados.")