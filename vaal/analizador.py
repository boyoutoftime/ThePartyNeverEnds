from transformers import pipeline

resumidor = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def resumir_textos(textos, max_palabras=300):
    todo = "\n\n".join(textos)
    partes = [todo[i:i+1000] for i in range(0, len(todo), 1000)]

    resumenes = []
    for parte in partes:
        resumen = resumidor(parte, max_length=200, min_length=50, do_sample=False)
        resumenes.append(resumen[0]['summary_text'])

    final = " ".join(resumenes)
    return final[:max_palabras*5]  # Limita largo final