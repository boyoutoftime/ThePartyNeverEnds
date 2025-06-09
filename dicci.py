import json

def generar_diccionario_ingles(archivo_txt, archivo_json):
    dic = {}
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            palabra = linea.strip().lower()
            if palabra:
                # No agregamos sinónimos aquí, solo la palabra
                dic[palabra] = []
    with open(archivo_json, 'w', encoding='utf-8') as f:
        json.dump(dic, f, indent=2, ensure_ascii=False)
    print(f"✅ Generado diccionario con {len(dic)} palabras")

if __name__ == "__main__":
    generar_diccionario_ingles("words.txt", "diccionario_base.json")