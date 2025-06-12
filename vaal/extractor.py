import fitz  # PyMuPDF  
import regex as re  
import sys  
import os  
import json  
  
# === Regex mejorada para expresiones embebidas ===  
ECUACION_REGEX = r"""  
(?<![\w/])                                # No precedido por palabra/slash  
(  
    [A-Za-zα-ωΑ-Ω0-9_]+                  # Variable tipo D2, αSMC, etc.  
    \s*(=|≈|∝)\s*                        # Operadores aceptados  
    (                                    # Comienza parte derecha  
        [-+*/^A-Za-z0-9().±×eE,−∞^°′″ ]+ # Números, símbolos y formatos científicos  
    )  
)  
(?![\w/])                                # No seguido por palabra/slash  
"""  
  
pattern = re.compile(ECUACION_REGEX, re.VERBOSE)  
  
def limpiar_ecuacion(ecuacion):  
    """  
    Limpia una ecuación eliminando paréntesis finales, puntos, comas  
    y convierte notación ×10n a notación exponencial clara.  
    """  
    ecuacion = ecuacion.strip()  
  
    # Quitar paréntesis o puntuación final  
    ecuacion = re.sub(r"[\s\.,;:)\]]+$", "", ecuacion)  
  
    # Convertir variantes como ×103 o × 10^3 a × 10^3  
    ecuacion = re.sub(r"×\s?10(\^?)(\d+)", r"× 10^\2", ecuacion)  
  
    return ecuacion  
  
def extraer_texto_del_pdf(pdf_path):  
    texto_completo = ""  
    doc = fitz.open(pdf_path)  
    for pagina in doc:  
        texto_completo += pagina.get_text()  
    return texto_completo  
  
def detectar_fragmentos(texto):  
    candidatos = []  
    lineas = texto.split("\n")  
  
    for linea in lineas:  
        linea = linea.strip()  
        if not linea:  
            continue  
  
        ecuaciones_crudas = [m.group(1) for m in pattern.finditer(linea)]  
        ecuaciones_limpias = [limpiar_ecuacion(e) for e in ecuaciones_crudas]  
  
        # Eliminar duplicados dentro de la misma línea  
        ecuaciones_unicas = list(sorted(set(ecuaciones_limpias)))  
  
        if ecuaciones_unicas:  
            candidatos.append({  
                "original": linea,  
                "ecuaciones": ecuaciones_unicas  
            })  
  
    return candidatos  
  
def guardar_salida(candidatos, archivo_salida):  
    with open(archivo_salida, "w", encoding="utf-8") as f:  
        json.dump(candidatos, f, indent=2, ensure_ascii=False)  
  
if __name__ == "__main__":  
    if len(sys.argv) < 2:  
        print("Uso: python extractor.py archivo.pdf")  
        sys.exit(1)  
  
    archivo_pdf = sys.argv[1]  
    if not os.path.exists(archivo_pdf):  
        print(f"[ERROR] Archivo no encontrado: {archivo_pdf}")  
        sys.exit(1)  
  
    print(f"[INFO] Extrayendo texto de: {archivo_pdf}")  
    texto = extraer_texto_del_pdf(archivo_pdf)  
  
    print("[INFO] Detectando fragmentos candidatos...")  
    fragmentos = detectar_fragmentos(texto)  
  
    archivo_salida = archivo_pdf.replace(".pdf", "_fragmentos.json")  
    guardar_salida(fragmentos, archivo_salida)  
  
    print(f"[OK] Fragmentos guardados en: {archivo_salida}")  
    print(f"[TOTAL]: {len(fragmentos)} fragmentos encontrados.")