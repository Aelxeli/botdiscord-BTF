from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from utils.config_manager import load_config, save_config
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'btf_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@socketio.on('update_config')
def handle_update_config(data):
    config = load_config()
    # Atualiza apenas os campos permitidos
    for key, value in data.items():
        if key in config:
            config[key] = value
    
    save_config(config)
    # Notifica todos os clientes (incluindo o Bot) sobre a mudança
    emit('config_updated', config, broadcast=True)
    print(f"Configuração atualizada via Dashboard: {data}")

def run_dashboard():
    socketio.run(app, port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_dashboard()
