# HUBI SERVER IA
# Creado por @flowese
# Powered by @hubspain
# Versión WhatsApp.

# Librerías
from os import system, getenv
from dotenv import load_dotenv
from flask import Flask, request, session, render_template, redirect
from flask_socketio import SocketIO, send, emit
from time import sleep
import datetime
# Librerías propias.
from api.api import funciones_chat
from funciones.hubi_core import variables_sistema, inicio_app

# Carga de variables de entorno.
fecha_now, hora_now, clave_secreta, server_port, server_ip, debug_server = variables_sistema()

# inicio por consola cross-check.
system('clear')
print (f'\n· HUBI VERSION: 1.5(dev)\n· FECHA ACTUAL: {fecha_now}\n· HORA ACTUAL: {hora_now}')

# Declaramos objeto Flask y socketio.
app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = clave_secreta
# Iniciamos dotenv para leer fichero de variables .env.
load_dotenv()

# Check por consola general de variables.
print (f'· PUERTO ACTIVO: {server_port}\n· IP ACTIVA: {server_ip}\n· DEBUG FLASK: {debug_server}\n· UNIKEY HUBI: {clave_secreta}')

# Rutas estáticas Flask.
# HTTP Hubi Index
@app.route('/', methods=['GET'])
def index():
    logpath = getenv("LOG_PATH")
    with open(f'{logpath}/chatlog.log', 'r') as weblogs:
        return render_template('index.html', textlog=weblogs.read()) 

# WEBHOOK Hubi Endpoint.
@app.route('/hubi', methods=['POST', 'GET'])
def mensajes():
    if request.method == "POST":
        # Leemos el mensaje de twilio de surespuesta selecionamos el contenido de 'Body'.
        incoming_msg = request.values['Body']
        # Intercambio de chat + Triggers personalizados.
        return funciones_chat(incoming_msg) # Función en fichero api/apy.py.
    else:
        # Return si se visita el webhook via http.
        return '¡Webhook de Hubi!'

# Webchat BETA
@app.route('/chat')
def webchat():
    return render_template('chat.html')

# WebSocket BETA
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

# CONTROL 404.
@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')

# inicio App
if __name__ == '__main__':
    inicio_app()
    # Iniciamos Hubi sobre el puerto 5000
    app.run(host=server_ip, port=server_port, debug=debug_server)
