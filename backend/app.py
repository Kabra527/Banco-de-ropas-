from flask_wtf.csrf import CSRFProtect

import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Cargar la clave secreta desde variable de entorno
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev')

csrf = CSRFProtect(app)


from flask import Flask, render_template, request, jsonify
from backend.services.services import DonationService
from backend.database import init_db
import logging

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Inicializar BD (crea tablas si no existen)
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/donacion')
def donacion_page():
    return render_template('donacion.html')

@app.route('/inventario')
def inventario_page():
    return render_template('inventario.html')

@app.route('/api/donaciones', methods=['GET'])
def listar_donaciones():
    try:
        items = DonationService.list_inventory()
        return jsonify(items), 200
    except Exception:
        app.logger.exception('Error al listar donaciones')
        return jsonify({'error': 'Error interno al listar donaciones'}), 500

@app.route('/api/donaciones', methods=['POST'])
def crear_donacion():
    try:
        data = request.get_json(force=True)
        tipo = data.get('tipo', '').strip()
        talla = data.get('talla', '').strip()
        cantidad = data.get('cantidad')
        if not tipo or not talla:
            return jsonify({'error': 'campo tipo y talla obligatorios'}), 400
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return jsonify({'error': 'cantidad debe ser un entero positivo'}), 400
        if cantidad <= 0:
            return jsonify({'error': 'cantidad debe ser mayor que 0'}), 400
        donation_id = DonationService.create_donation(tipo, talla, cantidad, data.get('descripcion',''))
        return jsonify({'id': donation_id}), 201
    except Exception:
        app.logger.exception('Error al crear donación')
        return jsonify({'error': 'Error interno al crear donación'}), 500

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)

