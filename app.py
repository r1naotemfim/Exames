from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


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

            posicoes = [m.start() for m in re.finditer(nome, texto)]

            for pos in posicoes:
                trecho = texto[pos:pos + 200]

                numeros = re.findall(r"\d+[.,]?\d*", trecho)

                # remove números muito grandes (datas etc)
                numeros = [n for n in numeros if len(n) <= 6]

                # remove números tipo 24/10
                numeros = [n for n in numeros if not n.startswith("24")]

                if numeros:
                    valor = numeros[0]

                    if not any(abrev in r for r in resultado):
                        resultado.append(f"{abrev} {valor}")
                        break

            if any(abrev in r for r in resultado):
                break

    return " // ".join(resultado)


@app.route("/processar", methods=["POST", "OPTIONS"])
def processar():
    if request.method == "OPTIONS":
        return '', 200

    dados = request.get_json()
    texto = dados.get("texto", "")

    resultado = extrair(texto)

    print("RESULTADO:", resultado)

    return jsonify({"resultado": resultado})


if __name__ == "__main__":
    app.run(debug=True)
