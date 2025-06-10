import os
import json
import sys
import re
import unicodedata
from lector import extraer_texto_de_pdf

if len(sys.argv) < 2:
    print("❌ Uso: python prueba.py <ruta_pdf>")
    exit()

PDF_PRUEBA = sys.argv[1]

def cargar_simbolos(ruta='simbolos_aprendidos.json'):
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_simbolos(diccionario, ruta='simbolos_aprendidos.json'):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, indent=2, ensure_ascii=False)

# Función que valida si el símbolo es válido para guardar
def es_simbolo_valido(s):
    if not s:  # vacío
        return False
    if not s.isprintable():  # caracteres no imprimibles (control, binarios)
        return False
    if s.isspace():  # espacios y similares
        return False
    # Obtenemos la categoría Unicode: 
    categoria = unicodedata.category(s)
    # 'Sm' = símbolo matemático, 'So' = símbolo otros, 'Sc' = símbolo moneda (opcionales)
    # Puedes ajustar qué categorías quieres aceptar:
    return categoria in ('Sm', 'So', 'Sc')

def es_ecuacion(linea):
    if "=" in linea or re.search(r"\b\d+(\.\d+)?\b", linea):
        simbolos = re.findall(r"[^\w\s]", linea)  # signos no alfanuméricos
        # filtramos los símbolos válidos según la función nueva
        simbolos_validos = [s for s in simbolos if es_simbolo_valido(s)]
        if len(simbolos_validos) / max(1, len(linea)) > 0.05:  # porcentaje ajustado
            return True
    return False

def extraer_simbolos(ecuacion):
    simbolos = set(re.findall(r"[^\w\s]", ecuacion))
    # filtramos solo símbolos válidos
    return sorted([s for s in simbolos if es_simbolo_valido(s)])

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
                    # Guardamos la categoría Unicode junto al símbolo
                    categoria = unicodedata.category(s)
                    simbolos_aprendidos[s] = f"Símbolo detectado en ecuación (Categoría Unicode: {categoria})"
                    print(f"➕ Nuevo símbolo aprendido: {s} (Categoría: {categoria})")

    guardar_simbolos(simbolos_aprendidos)
    print("\n✅ Lectura de ecuaciones completada. Símbolos guardados.")