from flask import Flask, render_template, request
from ai_engine import generar_caso, generar_solucion_ia, comparar_respuestas

app = Flask(__name__)

caso_actual = ""  # Variable global para almacenar el caso generado

@app.route("/")
def index():
    return render_template("index.html")  # Tu portada con el botón

@app.route("/generar", methods=["POST"])
def generar():
    global caso_actual
    caso_actual = generar_caso()  # Solo se genera aquí
    return render_template("generar.html", caso=caso_actual)  # Muestra el caso + input usuario

@app.route("/resolver", methods=["POST"])
def resolver():
    global caso_actual
    solucion_usuario = request.form["solucion_usuario"]
    solucion_ia = generar_solucion_ia(caso_actual)
    similitud, alineacion_usuario, alineacion_ia = comparar_respuestas(solucion_usuario, solucion_ia)
    return render_template("resultado.html",
                           caso=caso_actual,
                           solucion_usuario=solucion_usuario,
                           solucion_ia=solucion_ia,
                           similitud=similitud,
                           alineacion_usuario=alineacion_usuario,
                           alineacion_ia=alineacion_ia)

if __name__ == "__main__":
    app.run(debug=True)
