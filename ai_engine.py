import google.generativeai as genai
from difflib import SequenceMatcher

# 🔐 API Key de Google Gemini (obtenida en console.cloud.google.com)
API_KEY = "AIzaSyDVyjTOslSXKFiM4wHQtdh3k3pgI_hGtwM"
genai.configure(api_key=API_KEY)

# Usaremos el modelo Gemini Pro
MODEL = genai.GenerativeModel("gemini-1.5-pro-latest")


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

    try:
        response = MODEL.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error al generar el caso:", e)
        return "Error al generar el caso de estudio."


def generar_solucion_ia(caso):
    """
    Genera la solución usando IA con base en el caso generado.
    """
    prompt = (
        f"A partir del siguiente caso de estudio, proporciona una solución clara "
        f"siguiendo los principios de la norma ISO 42010:\n\n{caso}"
    )

    try:
        response = MODEL.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error al generar la solución:", e)
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
    Evalúa qué tan alineado está un texto con los principios de la norma ISO 42010.
    Devuelve un porcentaje entre 0 y 100, siendo 0 sin relación y 100 totalmente alineado.
    """
    prompt = (
        "Eres un experto en arquitectura de sistemas y conoces la norma ISO/IEC/IEEE 42010. "
        "Tu tarea es leer el siguiente texto y evaluar si está relacionado técnica y directamente con los principios de esta norma. "
        "Si el texto no menciona arquitectura, stakeholders, puntos de vista, modelos o conceptos claves de ISO 42010, responde 0. "
        "Si el texto aplica correctamente esos principios, responde con un porcentaje entre 0 y 100 según el nivel de alineación. "
        "Solo devuelve un número, sin explicaciones ni símbolos.\n\n"
        f"Texto:\n{texto}"
    )

    try:
        response = MODEL.generate_content(prompt)
        content = response.text.strip()
        return float(content.replace("%", "").replace(",", "."))
    except Exception as e:
        print("Error al evaluar alineación ISO 42010:", e)
        return 0.0
