import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime

# 1. Configuración para que Flask sepa dónde está el Frontend y los Assets
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app) # Permite que el HTML conecte con este servidor

DB_NAME = "citas.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            telefono TEXT,
            servicio TEXT,
            barbero TEXT,
            fecha TEXT,
            hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def limpiar_historial():
    """Elimina automáticamente las citas de días anteriores a hoy"""
    hoy = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservas WHERE fecha < ?", (hoy,))
    conn.commit()
    conn.close()


# ==========================================================
# RUTAS NUEVAS: Mostrar el diseño visual y las imágenes
# ==========================================================

@app.route('/')
def serve_index():
    """Entrega el index.html principal"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Entrega las imágenes (logos) de la carpeta assets"""
    assets_dir = os.path.join(app.static_folder, 'assets')
    return send_from_directory(assets_dir, filename)


# ==========================================================
# RUTAS DE LA API (Las que ya tenías funcionando)
# ==========================================================

@app.route('/api/agendar', methods=['POST'])
def agendar():
    datos = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Verificar que la hora no se haya tomado en el último segundo
    cursor.execute("SELECT id FROM reservas WHERE fecha = ? AND hora = ? AND barbero = ?", 
                  (datos['fecha'], datos['hora'], datos['barbero']))
    if cursor.fetchone():
        return jsonify({"error": "La hora ya fue tomada"}), 400

    cursor.execute('''
        INSERT INTO reservas (cliente, telefono, servicio, barbero, fecha, hora)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datos['cliente'], datos['telefono'], datos['servicio'], datos['barbero'], datos['fecha'], datos['hora']))
    
    conn.commit()
    conn.close()
    
    # Aquí iría tu: whatsapp.enviar_notificacion(...)
    
    return jsonify({"mensaje": "Cita agendada con éxito"}), 200

@app.route('/api/disponibilidad', methods=['GET'])
def disponibilidad():
    fecha = request.args.get('fecha')
    barbero = request.args.get('barbero')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Traer solo las horas que ya están ocupadas
    cursor.execute("SELECT hora FROM reservas WHERE fecha = ? AND barbero = ?", (fecha, barbero))
    ocupadas = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    
    return jsonify({"ocupadas": ocupadas})

@app.route('/api/citas', methods=['GET'])
def obtener_citas():
    limpiar_historial() # Borra lo viejo antes de mostrar
    fecha = request.args.get('fecha')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT cliente, servicio, hora, barbero, telefono FROM reservas WHERE fecha = ? ORDER BY hora", (fecha,))
    
    citas = []
    for fila in cursor.fetchall():
        citas.append({
            "cliente": fila[0],
            "servicio": fila[1],
            "hora": fila[2],
            "barbero": fila[3],
            "telefono": fila[4]
        })
    conn.close()
    
    return jsonify(citas)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
