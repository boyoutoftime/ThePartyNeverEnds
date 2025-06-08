from transformers import pipeline

# 🔹 Modelo de resumen (como ya tenías)
resumidor = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# 🔹 Modelo de pregunta-respuesta (nuestra red neuronal de comprensión)
qa = pipeline("question-answering", model="deepset/roberta-base-squad2")


def resumir_textos(textos, max_palabras=300):
    """
    Resume una lista de textos largos.
    """
    todo = "\n\n".join(textos)
    partes = [todo[i:i+1000] for i in range(0, len(todo), 1000)]

    resumenes = []
    for parte in partes:
        resumen = resumidor(parte, max_length=200, min_length=50, do_sample=False)
        resumenes.append(resumen[0]['summary_text'])

    final = " ".join(resumenes)
    return final[:max_palabras*5]  # Limita el largo final


def analizar_con_pregunta(texto: str, pregunta: str) -> str:
    """
    Usa una red neuronal para responder una pregunta específica sobre un texto.
    """
    try:
        respuesta = qa({
            'context': texto,
            'question': pregunta
        })
        return respuesta['answer']
    except Exception as e:
        return f"[Error en análisis]: {e}"