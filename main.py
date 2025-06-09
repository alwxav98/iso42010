from flask import Flask, render_template, request
from ai_engine import generar_caso, generar_solucion_ia, comparar_respuestas
import markdown
from flask import send_file
from xhtml2pdf import pisa
import io
import re
from PyPDF2 import PdfReader

app = Flask(__name__)

caso_actual = ""  # Variable global para almacenar el caso generado

@app.route("/")
def index():
    return render_template("index.html")  # Tu portada con el botón

@app.route("/generar", methods=["POST"])
def generar():
    global caso_actual
    caso_actual = generar_caso()  # Solo se genera aquí
    caso_html = markdown.markdown(caso_actual)
    return render_template("generar.html", caso=caso_html)  # Muestra el caso + input usuario

@app.route("/resolver", methods=["POST"])
def resolver():
    global caso_actual
    solucion_usuario = request.form["solucion_usuario"]
    solucion_ia = generar_solucion_ia(caso_actual)
    similitud, alineacion_usuario, alineacion_ia, analisis = comparar_respuestas(solucion_usuario, solucion_ia)
    
    caso_html = markdown.markdown(caso_actual)
    solucion_ia_html = markdown.markdown(solucion_ia)
    analisis_html = markdown.markdown(analisis)
    
    return render_template("resultado.html",
                           caso=caso_html,
                           solucion_usuario=solucion_usuario,
                           solucion_ia=solucion_ia_html,
                           similitud=similitud,
                           alineacion_usuario=alineacion_usuario,
                           alineacion_ia=alineacion_ia,
                           analisis=analisis_html)

def limpiar_listas_para_pdf(html):
    """
    Convierte listas HTML (<ul><li>) a párrafos simples (<p>) con viñetas.
    Compatible con xhtml2pdf.
    """
    html = html.replace('<ul>', '').replace('</ul>', '')
    html = html.replace('<ol>', '').replace('</ol>', '')
    html = re.sub(r'<li>(.*?)</li>', r'<p>• \1</p>', html)
    return html

@app.route("/descargar_pdf", methods=["POST"])
def descargar_pdf():
    caso = limpiar_listas_para_pdf(request.form["caso"])
    solucion_usuario = limpiar_listas_para_pdf(request.form["solucion_usuario"])
    solucion_ia = limpiar_listas_para_pdf(request.form["solucion_ia"])
    analisis = limpiar_listas_para_pdf(request.form["analisis"])

    rendered = render_template("pdf_template.html",
                               caso=caso,
                               solucion_usuario=solucion_usuario,
                               solucion_ia=solucion_ia,
                               analisis=analisis)

    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(rendered), dest=pdf_file)
    pdf_file.seek(0)

    if pisa_status.err:
        return "Hubo un error al generar el PDF", 500

    return send_file(pdf_file, as_attachment=True, download_name="informe_iso42010.pdf")


@app.route("/manual", methods=["GET"])
def manual():
    return render_template("manual.html")

@app.route("/procesar_manual", methods=["POST"])
def procesar_manual():
    global caso_actual

    # 1. Si viene texto manual
    caso_manual = request.form.get("caso_manual", "").strip()
    if caso_manual:
        caso_actual = caso_manual
    else:
        # 2. Si viene PDF, lo leemos
        archivo = request.files.get("caso_pdf")
        if archivo and archivo.filename.endswith(".pdf"):
            try:
                pdf = PdfReader(archivo)
                texto = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                caso_actual = texto
            except Exception as e:
                return f"Error al leer el PDF: {e}", 500
        else:
            return "No se ingresó un texto ni se subió un archivo válido.", 400

    caso_html = markdown.markdown(caso_actual)
    return render_template("generar.html", caso=caso_html)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
