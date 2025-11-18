from flask import Flask, jsonify
from db import get_connection
from queries import CONSULTAS

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "OK", "message": "API funcionando"}

@app.route("/api/<string:consulta>")
def ejecutar(consulta):
    if consulta not in CONSULTAS:
        return jsonify({"error": "Consulta no encontrada"}), 404

    sql = CONSULTAS[consulta]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    colnames = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    resultado = [dict(zip(colnames, row)) for row in rows]

    return jsonify(resultado)
