from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# =========================
# FUNÇÃO
# =========================
def extrair(texto):
    texto = texto.lower()

    exames = {
        "Hb": ["hemoglobina"],
        "Ht": ["hematócrito", "hematocrito"],
        "Leuco": ["leucócitos", "leucocitos"],
        "Plq": ["plaquetas"],

        "Cr": ["creatinina"],
        "Ur": ["uréia", "ureia"],
        "Na": ["sódio", "sodio"],
        "K": ["potássio", "potassio"],

        "PCR": ["proteína c reativa", "pcr"],
        "INR": ["inr"],
        "TTPA": ["tromboplastina parcial"],

        "Albumina": ["albumina"],
        "Ca": ["cálcio", "calcio"]
    }

    resultado = []

    for abrev, nomes in exames.items():
        for nome in nomes:
            for m in re.finditer(nome, texto):
                trecho = texto[m.start():m.start() + 200]

                numeros = re.findall(r"\d+[.,]?\d*", trecho)

                numeros = [n for n in numeros if not n.endswith(".")]

                if numeros:
                    valor = numeros[0]

                    if not any(abrev in r for r in resultado):
                        resultado.append(f"{abrev} {valor}")
                        break

            if any(abrev in r for r in resultado):
                break

    return " // ".join(resultado)

# =========================
# FRONTEND
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# API
# =========================
@app.route("/processar", methods=["POST", "OPTIONS"])
def processar():
    if request.method == "OPTIONS":
        return '', 200

    dados = request.get_json()
    texto = dados.get("texto", "")

    resultado = extrair(texto)

    return jsonify({"resultado": resultado})

# =========================
# START
# =========================
if __name__ == "__main__":
    app.run(debug=True)
