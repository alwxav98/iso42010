import google.generativeai as genai
from difflib import SequenceMatcher
import os
from dotenv import load_dotenv

# 🔐 API Key de Google Gemini (obtenida en console.cloud.google.com)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
print("API_KEY cargada:", API_KEY)
# Usaremos el modelo Gemini Pro
MODEL = genai.GenerativeModel("gemini-2.0-flash-lite-001")
#response = MODEL.generate_content("Solo dime: ¿qué hora es?")
#print(response.text)


def generar_caso():
    """
    Genera solo el caso de estudio basado en la norma ISO 42010.
    """
    prompt = (
        "Genera un caso de estudio único en cualquier campo, nuevo y diferente que sea técnico y realista enfocado exclusivamente en la aplicación de la norma ISO 42010. "
        "Debe representar una situación en una organización que requiere aplicar esta norma para definir o gestionar "
        "la arquitectura de un sistema complejo. Describe claramente el contexto, el problema y los involucrados. "
        "NO incluyas la solución aún. El caso debe ser claro y profesional."
    )

    try:
        response = MODEL.generate_content(prompt, generation_config={"temperature": 0.9})
        return response.text.strip()
    except Exception as e:
        print("Error al generar el caso:", e)
        return "Error al generar el caso de estudio."


def generar_solucion_ia(caso):
    """
    Genera la solución usando IA con base en el caso generado.
    """
    prompt = (
        f"A partir del siguiente caso de estudio, proporciona una solución clara, no incluyas tablas "
        f"siguiendo los principios de la norma ISO 42010:\n\n{caso}"
    )

    try:
        response = MODEL.generate_content(prompt, generation_config={"temperature": 0.9})
        return response.text.strip()
    except Exception as e:
        print("Error al generar la solución:", e)
        return "No se pudo generar la solución del caso."


def comparar_respuestas(usuario, ia):
    """
    Compara las soluciones y devuelve:
    - Porcentaje de similitud
    - Alineación de usuario e IA
    - Análisis comparativo generado por IA
    """
    similitud = SequenceMatcher(None, usuario.strip().lower(), ia.strip().lower()).ratio()
    porcentaje_similitud = round(similitud * 100, 2)

    alineacion_usuario = evaluar_alineacion_iso42010(usuario)
    alineacion_ia = evaluar_alineacion_iso42010(ia)

    analisis = analizar_respuestas(usuario, alineacion_usuario, ia, alineacion_ia)

    return porcentaje_similitud, alineacion_usuario, alineacion_ia, analisis



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
    
def analizar_respuestas(respuesta_usuario, alineacion_usuario, respuesta_ia, alineacion_ia):
    """
    Solicita a Gemini un análisis comparativo entre ambas respuestas respecto a la norma ISO 42010.
    """
    prompt = (
        "Actúa como un experto en arquitectura de sistemas y cumplimiento de normas ISO. "
        "Analiza las dos respuestas que se presentan a continuación. "
        "Ambas intentan dar solución a un caso técnico basado en la norma ISO 42010.\n\n"
        f"Respuesta del usuario (alineación: {alineacion_usuario}%):\n{respuesta_usuario}\n\n"
        f"Respuesta de la IA (alineación: {alineacion_ia}%):\n{respuesta_ia}\n\n"
        "Tu tarea es indicar cuál de las dos respuestas está más alineada con la norma ISO 42010 y justificar por qué. "
        "Además, comenta cuál tiene mayor aceptación profesional y explica brevemente las fortalezas y debilidades de cada una. "
        "Finaliza tu respuesta con un resumen que diga cuál es la más adecuada en este contexto y por qué."
    )

    try:
        response = MODEL.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error al generar el análisis comparativo:", e)
        return "No se pudo generar el análisis comparativo entre las respuestas."

