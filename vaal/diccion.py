import json

def cargar_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

base = cargar_json("diccionario_base.json")
especial = cargar_json("terminos_cientificos.json")

# Une el español y los técnicos debajo
for clave, valores in especial.items():
    base[clave.lower()] = valores

with open("diccionario_total.json", 'w', encoding='utf-8') as f:
    json.dump(base, f, indent=2, ensure_ascii=False)

print(f"Diccionario total listo con {len(base)} entradas")