# HUBI API / WEBHOOK.
# ENDPOINT WEBHOOK: https://code.hubspain.com/hubi
# by @flowese
# powered by @hubspain


# Librerías
import os
from os import system, getenv
from dotenv import load_dotenv
import datetime
from threading import Thread
from flask import Flask, request, session, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse as twilioMensRecep
from flask_socketio import SocketIO, send
from funciones.hubi_core import sentencia, memoria_interaccion, reset_memoria, help
from funciones.custom import ping, status_services, manage_services, currency, whatsapp_send, alarma
from time import sleep


# Path de los logs definido en fichero .env.
logpath = getenv("LOG_PATH")

# Check por consola
print ('· ESTADO API HUBI: OK')


# Insertar chat en log.
def insert_logchat(incoming_msg, answer):
    now = datetime.datetime.now()
    fechalog = (now.strftime("%Y-%m-%d %H:%M:%S"))
    logfile = open (f'{logpath}/chatlog.log','a') 
    logfile.write(str(f'\n{fechalog} - Persona: {incoming_msg} \n{fechalog} - Hubi: {answer}\n'))
    logfile.close()

# Funciones de Chat.
def funciones_chat(incoming_msg):
    if '/holamundo' in incoming_msg: #MAIN
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split()
        comando = cadenasplit
        chat_log = session.get('chat_log')
        now = datetime.datetime.now()
        hora = (now.strftime("%H:%M:%S"))
        answer = f'Hola soy Hubi parece que todo funciona con normalidad. Ahora son las {hora}, hora española.'
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg)
    # Función Ping #CUSTOM
    if '/ping' in incoming_msg:
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split()
        comando, host = cadenasplit
        chat_log = session.get('chat_log')
        answer = ping(host)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg)
    # Enviar WhatsApp. #CUSTOM
    if '/wasap' in incoming_msg or '/whatsapp' in incoming_msg:
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split(' ',2)
        comando, destino, mensaje = cadenasplit
        chat_log = session.get('chat_log')
        twil_Num =  '+14155238886'
        answer = whatsapp_send(twil_Num, destino, mensaje)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg) 
    # Estado de los servicios. #CUSTOM
    if '/status' in incoming_msg or '/estado' in incoming_msg:
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split()
        comando, service = cadenasplit
        chat_log = session.get('chat_log')
        answer = status_services(service)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg)
    # Coindesk API. #CUSTOM
    if '/coin' in incoming_msg or '/currency' in incoming_msg:
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split()
        consulta, coin = cadenasplit
        chat_log = session.get('chat_log')
        answer = currency(coin)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg)
            
    # Manejar Servicios. #CUSTOM
    if '/service' in incoming_msg or '/servicio' in incoming_msg:
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split()
        comando, state, service = cadenasplit
        chat_log = session.get('chat_log')
        answer = manage_services(state, service)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg) 
    # Directorio Ayuda. #MAIN
    if '/help' in incoming_msg or '/ayuda' in incoming_msg:
        incoming_msg = request.values['Body']
        chat_log = session.get('chat_log')
        answer = help()
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg)
    # Reiniciar memoria de Hubi. #MAIN
    if '/restart mem' in incoming_msg or '/reset mem' in incoming_msg or '/set mem' in incoming_msg:
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split()
        comando, mem, tipo_memoria = cadenasplit
        chat_log = session.get('chat_log')
        answer = reset_memoria(tipo_memoria)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg)
        
        # PLEX SERVICE GPT-3 BETA. #CUSTOM HYBRID
    if 'reinicia plex' in incoming_msg or 'reiniciar plex' in incoming_msg or 'reinicies plex' in incoming_msg or 'reiniciame plex' in incoming_msg:
        incoming_msg = request.values['Body']
        chat_log = session.get('chat_log')
        manage_services('stop', 'watchtower')
        print('La tarea se ha ejecutado.')
        sleep(20)
        manage_services('start', 'watchtower')
        print('La tarea ha terminado!!')
        # GPT-3 sentencia
        answer = incoming_msg
        answer = sentencia(incoming_msg, chat_log)
        session['chat_log'] = memoria_interaccion(incoming_msg, answer, chat_log)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación.
        insert_logchat(incoming_msg, answer)
        return str(msg)

        
        # Enviar WhatsApp. #CUSTOM
    if '/alarma' in incoming_msg:
        incoming_msg = request.values['Body']
        cadenasplit = incoming_msg.split(' ',4)
        comando, destino, hora, minutos, motivo = cadenasplit
        answer = Thread(target= alarma, args=(destino, hora, minutos, motivo))
        answer.start()
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación + trigger.
        insert_logchat(incoming_msg, answer)
        return str(msg) 

    # Intercambio de chat normal con Hubi.
    # GPT-3. #MAIN
    else:
        incoming_msg = request.values['Body']
        chat_log = session.get('chat_log')
        answer = sentencia(incoming_msg, chat_log)
        session['chat_log'] = memoria_interaccion(incoming_msg, answer, chat_log)
        msg = twilioMensRecep()
        msg.message(answer)
        # Guardamos los logs de conversación.
        insert_logchat(incoming_msg, answer)
        return str(msg)