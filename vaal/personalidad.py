def dar_estilo(texto, tono="profesional", firma=False):
    if tono == "profesional":
        estilo = f"Informe generado con enfoque académico:\n\n{texto}"
    elif tono == "curioso":
        estilo = f"¡Qué tema tan fascinante! Aquí tienes lo que encontré:\n\n{texto}"
    else:
        estilo = texto

    if firma:
        estilo += "\n\n-- IA Investigadora Alfa"
    
    return estilo