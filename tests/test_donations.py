import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from backend.app import app, init_db  # ✅ Import corregido

@pytest.fixture
def client():
    # Configuración para usar base de datos temporal o de prueba
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_create_and_list(client):
    # Crear una donación
    rv = client.post('/api/donaciones', json={
        'tipo': 'Camisa',
        'talla': 'M',
        'cantidad': 3
    })
    assert rv.status_code == 201  # Verifica creación exitosa

    # Obtener lista de donaciones
    res = client.get('/api/donaciones')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert any(d['tipo'] == 'Camisa' for d in data)
