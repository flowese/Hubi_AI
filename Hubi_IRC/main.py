# HUBI SERVER IA
# Creado por @flowese
# Powered by @hubspain
# Versión IRC.

# Librerías.
import pydle
from os import getenv
from dotenv import load_dotenv
from time import sleep
import datetime
import random
# Librerías propias.
from funciones.hubi import gpt3_consulta
from funciones.system import limpiar_terminal, help

# Conexión con Pydle Servidor IRC.
class MyOwnBot(pydle.Client):
    # Conectar al servidor y al canal por defecto.
    async def on_connect(self):
        await self.join(canal_defecto)
        print('Conectado correctamente al canal por defecto.')
    # Gestión de mensajes recibidos con Pydle.
    async def on_message(self, target, source, message): # source: Remitente del mensaje. # target: Destino del mensaje. # message: Contenido del mensaje.
        global admin
        global victima
        global nombre_bot
        global canal
        nombre_persona = source
        print ('>> Mensaje Recibido.')
        print(f'{source}: {message}')
        # Gestión de contenido de mensajes.
        if target == nombre_bot:
            if source == victima and target != admin:
                aviso = f'{source} ha mandado un privado a {nombre_bot}: {message}'
                # Aviso al administrador de mensaje privado.
                await self.message(admin, aviso)
            else:
                mens = f'>>> Se ha descartado el mensaje de {source} porque no es una víctima para {nombre_bot}.'
                # Insertar en log.
                await insert_logmeta(source,message, nombre_bot, mens, target)
        # Comandos del bot para administrador.
        if source == admin:
            # Función test.
            if '@test' in message:
                now = datetime.datetime.now()
                hora = (now.strftime("%H:%M:%S"))
                answer = f'Hola soy {nombre_bot}.\n· Todo funciona con normalidad.\n· Actualmente son las {hora}.'
                await self.message(admin,answer)
            # Mostrar Ayuda.
            if '@ayuda' in message or '@help' in message:
                menu = help()
                await self.message(admin, menu)
            # Cambiar de canal.
            if '@canal' in message or '@can' in message:
                cadenasplit = message.split()
                comando, canal = cadenasplit
                await self.join(canal)
                print (f'SISTEMA: {admin} ha cambiado al bot al canal {canal}.')
                response = f'SISTEMA: {admin} ha cambiado al bot al canal {canal}.'
                await self.message(admin, response)
                # Insertar en log.
                await insert_logmeta(source,message, nombre_bot, response)
            # Información del usuario.
            if '@usuarios' in message: # En desarrollo!!!!!
                info = await self.whois(source)
                #await self.message(admin, info)
                print (info)
            # Seleccionar víctima.
            if '@vic' in message:
                response = f'SISTEMA: {admin} a configurado una nueva víctima: {victima}.'
                cadenasplit = message.split()
                comando, victima = cadenasplit
                victima = victima
                await self.message(admin, response)
                # Insertar en log.
                await insert_logmeta(source,message, nombre_bot, response)
            # Enviar mensaje privado.
            if '@send' in message:
                cadenasplit = message.split(' ',2)
                comando, victima, mensaje = cadenasplit
                await self.message(victima, mensaje)
                response = f'SISTEMA: {admin} ha mandado el mensaje: {mensaje} a {victima}.'
                await self.message(admin, response)
                # Insertar en log.
                await insert_logmeta(source,message, nombre_bot, response)
            # Mostrar la configuración del bot.
            if '@config' in message:
                try:
                    canal
                except NameError:
                        cadenasplit = message.split()
                        comando, canal = cadenasplit
                        checkeo = f'CONFIGURACIÓN DEL BOT:\n· Servidor: {servidor}\n· Canal: {canal}\n· Nombre del Bot: {nombre_bot}\n· Administrador del Bot: {admin}\n· Víctima: {victima}\n'
                        await self.message(admin, checkeo)
                else:
                    checkeo = f'· Servidor: {servidor},\n· Canal: {canal}\n· Nombre del Bot: {nombre_bot}\n· Administrador del Bot: {admin}\n· Víctima: {victima}\n'
                    await self.message(admin, checkeo)
        # Verificamos la identidad de la victima != admin.            
        if source == victima and source != admin:
            # Simulamos de 7 a 20 (random) segundos de escritura.
            sim_escritura = random.randint(7, 20)
            print(f'>>> Esperando {sim_escritura} segundos para responder.')
            sleep(sim_escritura)
            # Enviar consulta a Hubi GPT-3.
            response = await gpt3_consulta(nombre_bot, nombre_persona, message)
            await insert_logmeta(source,message, nombre_bot, response)
            await self.message(source, response)
            print ('>>> Respuesta enviada al destino.')
            print(f'{nombre_bot}: {response}')
            aviso = f'{nombre_bot} ha mandado un privado a {source}: {response}'
            await self.message(admin, aviso)
        else:
            target = canal
            print (f'>> Mensaje general descartado por {nombre_bot}.')
            await insert_logmeta(canal, message=f'--> {source}: {message}', nombre_bot=f'', response=f'', target=target)

# Insertar datos en log.
async def insert_logmeta(source,message, nombre_bot, response, target=None):
    now = datetime.datetime.now()
    fechalog = (now.strftime("%Y-%m-%d %H:%M:%S"))
    # Fichero log para canales.
    if target == canal:
        logfile = open (f'logs/canales/{source}.log','a', encoding='utf-8')
        logfile.write(str(f'\n{fechalog} - {source}: {message}'))
        logfile.close()
    else:
        # Fichero log para usuarios.
        logfile = open (f'logs/usuarios/{source}.log','a', encoding='utf-8')
        logfile.write(str(f'\n{fechalog} - {source}: {message} \n{fechalog} - {nombre_bot}: {response}'))
        logfile.close()

# Iniciar App.
if __name__ == '__main__':
    # Cargar variables de entorno.
    load_dotenv()
    limpiar_terminal()
    servidor = getenv("IRC_SERVER")
    canal_defecto = getenv("IRC_CANAL_DEFECTO")
    nombre_bot = getenv("NOMBRE_BOT")
    admin = getenv("ADMIN_BOT")
    victima = admin
    canal = canal_defecto
    # Checkeo por terminal.
    print ('-INICIANDO HUBI BOT IRC-\n')
    checkeo_terminal = f'Servidor: {servidor}\nCanal por defecto: {canal_defecto}\nNombre del Bot: {nombre_bot}\nAdministrador del Bot: {admin}\nVíctima por defecto: {victima}\n'
    print (checkeo_terminal)
    client = MyOwnBot(nombre_bot, realname=nombre_bot)
    client.run(servidor, tls=True, tls_verify=False)