import requests
from difflib import SequenceMatcher

API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
MODEL = "openai/gpt-3.5-turbo"
MAX_TOKENS = 500


def generar_caso():
    """
    Genera solo el caso de estudio basado en la norma ISO 42010.
    """
    prompt = (
        "Genera un caso de estudio técnico y realista enfocado exclusivamente en la aplicación de la norma ISO 42010. "
        "Debe representar una situación en una organización que requiere aplicar esta norma para definir o gestionar "
        "la arquitectura de un sistema complejo. Describe claramente el contexto, el problema y los involucrados. "
        "NO incluyas la solución aún. El caso debe ser claro y profesional."
    )

    response = requests.post(BASE_URL, headers=HEADERS, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    })

    print("Respuesta al generar caso:", response.text)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error al procesar el caso:", e)
        return "Error al generar el caso de estudio."


def generar_solucion_ia(caso):
    """
    Genera la solución usando IA con base en el caso generado.
    """
    prompt = (
        f"A partir del siguiente caso de estudio, proporciona una solución clara "
        f"siguiendo los principios de la norma ISO 42010:\n\n{caso}"
    )

    response = requests.post(BASE_URL, headers=HEADERS, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600
    })

    print("Respuesta al generar solución:", response.text)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error al procesar la solución:", e)
        return "No se pudo generar la solución del caso."


def comparar_respuestas(usuario, ia):
    """
    Compara las soluciones y devuelve porcentaje de similitud + alineación con ISO 42010.
    """
    similitud = SequenceMatcher(None, usuario.strip().lower(), ia.strip().lower()).ratio()
    porcentaje_similitud = round(similitud * 100, 2)

    alineacion_usuario = evaluar_alineacion_iso42010(usuario)
    alineacion_ia = evaluar_alineacion_iso42010(ia)

    return porcentaje_similitud, alineacion_usuario, alineacion_ia


def evaluar_alineacion_iso42010(texto):
    """
    Evalúa qué tan alineado está un texto con la norma ISO 42010 (porcentaje).
    """
    prompt = (
        "Analiza el siguiente texto y evalúa qué tan alineado está con los principios de la norma ISO 42010. "
        "Devuélveme solo un número porcentual (sin símbolos ni explicaciones) entre 0 y 100.\n\n"
        f"Texto:\n{texto}"
    )

    response = requests.post(BASE_URL, headers=HEADERS, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 10
    })

    try:
        content = response.json()["choices"][0]["message"]["content"]
        return float(content.strip().replace("%", "").replace(",", "."))
    except Exception as e:
        print("Error al evaluar alineación ISO 42010:", e)
        return 0.0
