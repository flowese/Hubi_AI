# Custom triggers para HUBSPAIN.
# by @flowese
# powered by @hubspain

# Librerías
import os
import platform
import subprocess
import socket
import requests
from dotenv import load_dotenv
from twilio.rest import Client
from time import localtime
from funciones.hubi_core import sentencia, sentencia_custom

# Check por consola
print ('· FUNCIONES CUSTOM HUBI: OK')
# Importamos variables de entorno Twilio del fichero .env.
twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
print (f'· TWILIO SID: {twilio_account_sid}\n· TWILIO AUTH: {twilio_auth_token}')


# Trigger de Alarma con GPT-3.
def alarma(destino, hora, minutos, motivo):
    while True:
        if localtime().tm_hour == int(hora) and localtime().tm_min == int(minutos):
            # GPT-3 sentencia
            answer = sentencia_custom(motivo)
            twil_Num =  '+14155238886'
            whatsapp_send(twil_Num, destino, answer)
            break
    #return f'Se ha fijado la alarma para las {hora}:{minutos}.'

# Enviar WhatsApp a numero.
def whatsapp_send(num_origen,destino, mensaje):
    agenda = {"marc": 620417037, "rafa": 646921039, "nika": 666995062, "alex": 607357273}

    contacto = (agenda[destino])

    if destino in agenda:
        client = Client(twilio_account_sid, twilio_auth_token)
        if destino == 'marc' or destino == 'rafa' or destino == 'alex' or destino == 'nika':
            message = client.messages.create(
                              from_=f'whatsapp:{num_origen}',
                              body=f'{mensaje}',
                              to=f'whatsapp:+34{contacto}'
                          )
        else:
            return f'No se puede enviar el WhatsApp a {destino} porque no existe en la agenda.'
    return f'Mensaje {mensaje} para {destino} enviado.'


# Función hacer ping a un host.
def ping(host):
    parameter = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)
    if response == 0:
        return f'{host} parece estar en linea y responde a ping.'
    else:
        return f'Sin respuesta de {host} \nParece que el host no se encuentra disponible.'

# Función price data desde API Coindesk.
def currency(coin):
    # Lista de servicios.
    coins = ['btc', 'eth']
    if coin in coins:
        # PlexMediaServer Check.
        if coin == 'btc':
            response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
            data = response.json()
            coin_select = (data["bpi"]["USD"]["rate"]) 
            return f'El precio del Bitcoin es {coin_select}$'
    else:
        return f'De momento no hay información sobre {coin}.'

# Función consulta estado servicios HubSpain.com.
def status_services(service):
    # Lista de servicios.
    services = ['plex', 'solicitudes']
    if service in services:
        # PlexMediaServer Check.
        if service == 'plex':
            host='10.10.10.11'
            port=32400
            timeout_seconds=1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout_seconds)
            result = sock.connect_ex((host,int(port)))
            if result == 0:
                sock.close()
                return f'El {service} está en linea'
            else:
                sock.close()
                return f'El {service} no responde'
    else:
        return f'El servicio {service} no existe en hubspain.'

# Gestión de servicios HubSpain.com.
def manage_services(state, service):
    # Lista de servicios HubSpain.
    services = ['plex', 'netdata', 'tautulli', 'organizr', 'ogpagent', 'code-hub', 'portainer', 'deemix', 'overseerr', 'watchtower', 'tinymediamanager']
    # Estados únicos.
    states = ['start', 'stop']
    if service in services and state in states:
        # PlexMediaServer Container Service.
        if service == 'plex':
            command = ['docker', state, 'PlexMediaServer']
            response = subprocess.call(command)
            return f'{state} {service} se ha ejecutado.'
        # Netdata-Dashboard Container Service.
        if service == 'netdata':
            command = ['docker', state, 'Netdata-Dashboard'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'

        # Tautulli Container Service.
        if service == 'tautulli':
            command = ['docker', state, 'Tautulli'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'

        # Organizr Container Service.
        if service == 'organizr':
            command = ['docker', state, 'Organizr'] 
            response = subprocess.call(command)
            return f'{state} {service} se ha ejecutado.'

        # OpenGamePanel-Agent Container Service.
        if service == 'ogpagent':
            command = ['docker', state, 'OpenGamePanel-Agent'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'

        # Code-Hub Container Service.
        if service == 'code-hub' or service == 'codehub':
            command = ['docker', state, 'Code-Hub'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'

        # portainer Container Service.
        if service == 'portainer':
            command = ['docker', state, 'portainer'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'

        # Deemix Container Service.
        if service == 'deemix':
            command = ['docker', state, 'Deemix'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'

        # Overseerr Container Service.
        if service == 'overseer':
            command = ['docker', state, 'Overseer'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'

        # Watchtower Container Service.
        if service == 'watchtower':
            command = ['docker', state, 'WatchTower'] 
            response = subprocess.call(command)
            return f'{state} {service} se ha ejecutado.'

        # TinyMediaManager Container Service.
        if service == 'tinymediabox':
            command = ['docker', state, 'TinyMediaManager'] 
            response = subprocess.call(command) 
            return f'{state} {service} se ha ejecutado.'
    else:
        return f'El servicio o estado definido no existe en hubspain.'
