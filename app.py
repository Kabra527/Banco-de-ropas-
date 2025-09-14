from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)


DB_NAME = "bancode_ropas.db"

# ----------------------------
# Inicializar BD
# ----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT,
                    cantidad INTEGER,
                    estado TEXT
                )''')
    conn.commit()
    conn.close()

# ----------------------------
# Rutas HTML
# ----------------------------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/donacion')
def donacion():
    return render_template("donacion.html")

@app.route('/inventario')
def inventario():
    return render_template("inventario.html")

# ----------------------------
# API de Donaciones
# ----------------------------
@app.route('/api/donaciones', methods=['GET'])
def listar_donaciones():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM donaciones")
    donaciones = c.fetchall()
    conn.close()
    return jsonify(donaciones)

@app.route('/api/donaciones', methods=['POST'])
def agregar_donacion():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO donaciones (tipo, cantidad, estado) VALUES (?, ?, ?)",
              (data['tipo'], data['cantidad'], data['estado']))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Donación registrada con éxito"}), 201

# ----------------------------
# Main
# ----------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
