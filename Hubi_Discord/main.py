#Importamos libererías necesarias.
import discord, openai
from dotenv import load_dotenv
import os, datetime, random, subprocess
import urllib.request
import re

from wikipedia.wikipedia import search
from funciones.thispersondoesnotexist import Person
import wikipedia

#Definimos bot.
bot = discord.Client() 
#Cargamos variables de entorno.
load_dotenv()
#Discord token.
discord_token = os.getenv('DISCORD_TOKEN_BOT')
#GPT-3 API key.
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()
#Path foto de perfil de Discord.
path_img = os.getenv('PATH_IMG')
#Path Chatlog.
path_chatlog = os.getenv('PATH_CHATLOG')
#Path fichero personalidad.
path_persona = os.getenv('PATH_PERSONA')

#LOGS
#Almacena todas las conversaciones en fichero /config/chat.log.
def save_chat(chat_log):
    with open(path_chatlog, 'a', encoding='utf-8') as f:
        f.write(chat_log)
        f.write('\n')
        f.close()

#Lee el fichero chat.log y devuelve una lista con las conversaciones.
def read_chat():
    with open(path_chatlog, 'r', encoding='utf-8') as f:
        chatlog = f.read()
        f.close()
    return chatlog

#GPT-3
#Variables GPT-3.
start_sequence = '\nHubi:'
restart_sequence = f'\n\nPersona:'
#Cargamos fichero de personalidad.
with open(path_persona, 'r', encoding='utf-8') as f:
        session_prompt = f.read()
        f.close()

#Función y parámetros de consulta GPT-3.
def ask(question, chat_log=None):
 prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
 response = openai.Completion.create(
 engine='davinci',
 prompt=prompt_text,
 temperature=0.8,
 max_tokens=150,
 top_p=1,
 frequency_penalty=0,
 presence_penalty=0.3,
 stop=['\n'],
 )
 story = response['choices'][0]['text']
 return str(story)

#Función de modelo de Fine-tuning GPT-3.
''' ****PENDIENTE IMPLEMENTAR****
def ask_finetune(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    openai.Completion.create(
    model=FINE_TUNED_MODEL,
    prompt=prompt_text)
'''
#EVENTOS
#Al iniciar el bot, se ejecuta la función "on_ready".
@bot.event
async def on_ready():
    global path_img
    #Actividad del bot en discord
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='')) #Cambiar el estado aquí.
    #Muestra que el bot está conectado a tu token y a la API de Discord
    print('Bot iniciado como: {}'.format(bot.user.name)) 
    
    #Obtener una persona no real generada con IA (foto de perfil).
    person = Person(fetch_online=True)
    #Guarda la imagen de la persona en el directorio contenido.
    person.save(path_img)
    #Leer ruta de la imagen.
    file = open(path_img, 'rb')
    #Cambiar la imagen del bot si el número aleatorio está en el rango 1-10.
    if random.randint(1,5) == 1:
        await bot.user.edit(avatar=file.read())
    #Cierra el archivo.
    file.close()



#Al recibir un mensaje, se ejecuta la función "on_message".
@bot.event
async def on_message(message):
    #solo contestar a los usuarios registrados en contenido/whitelist.txt
    if message.author.name in open('Hubi_Discord/contenido/whitelist.txt').read().splitlines():
        #Si se menciona al bot contestar.
        for x in message.mentions:
            if(x==bot.user):
                #Rececpción de la consulta para GPT-3 en menciones al bot.
                chat_history = read_chat()
                chat_log=session_prompt+chat_history
                answer = ask(message.content, chat_log)
                now = datetime.datetime.now()
                fechalog = (now.strftime("%Y-%m-%d %H:%M:%S"))
                #Si la respuesta está vacía, envía nuevamente la consulta a GPT-3.
                if len(answer) < 1:
                    answer = ask(message.content, chat_log)
                    print('Reenviando consulta a GPT-3...')
                    await message.channel.send(answer)
                await message.channel.send(answer)

        now = datetime.datetime.now()
        fechalog = (now.strftime("%Y-%m-%d %H:%M:%S")) 
        mensaje = f'{fechalog} - {message.author}: {message.content}'
        global Persona
        Persona = message.author
        save_chat(mensaje)

        #Si el mensaje es del propio bot, no hacer nada.
        if message.author == bot.user:
            return
        #Si el mensaje DM contestar al mensaje.
        ''' ***PENDIENTE REVISAR***
        if message.channel.type == discord.ChannelType.private:
                chat_history = read_chat()
                chat_log=session_prompt+chat_history
                answer = ask(message.content, chat_log)
                now = datetime.datetime.now()
                fechalog = (now.strftime("%Y-%m-%d %H:%M:%S"))
                #Si la respuesta está vacía, envía nuevamente la consulta a GPT-3.
                if len(answer) < 1:
                    answer = ask(message.content, chat_log)
                    print('Reenviando consulta a GPT-3...')
                    await message.channel.send(answer)
                await message.channel.send(answer)
        '''

        #COMANDOS
        #Añadir usuario a la whitelist con el comando !whitelist add <usuario> o borrar usuario con !whitelist remove <usuario>
        if message.content.startswith('!whitelist add'):
            with open('Hubi_Discord/contenido/whitelist.txt', 'a') as f:
                user = message.content.split()[2]
                await message.channel.send(f'Añadiendo usuario {user} a la whitelist...')
                f.write('\n')
                f.write(user)
                f.close()
                await message.channel.send(f'Usuario {user} añadido correctamente.')
        if message.content.startswith('!whitelist remove') or message.content.startswith('!whitelist rem'):
            with open('Hubi_Discord/contenido/whitelist.txt', 'r') as f:
                user = message.content.split()[2]
                await message.channel.send(f'Borrando usuario {user} de la whitelist...')
                lines = f.readlines()
                f.close()
            with open('Hubi_Discord/contenido/whitelist.txt', 'w') as f:
                for line in lines:
                    if user not in line:
                        f.write(line)
                f.close()
            await message.channel.send(f'Usuario {user} borrado correctamente.')
        #Realiza una búsqueda en youtube y devuelve los resultados.
        if message.content.startswith('!youtube'):
            search_keyword = message.content[9:]
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            await message.channel.send(f'https://www.youtube.com/watch?v={video_ids[0]}')

        #Contesta al mensaje con el tiempo actual con el comando !time.
        if message.content.startswith('!time'):
            await message.channel.send(datetime.datetime.now().strftime("Actualmente son las %H:%M:%S"))
        #Contesta con la previsión del tiempo api openweathermap con el comando !weather.
        if message.content.startswith('!weather'):
            await message.channel.send('https://www.google.es/search?q=previsi%C3%B3n+del+tiempo')

        #Buscar en wikipedia api en español el comando !wiki palabra.
        if message.content.startswith('!wiki'):
            #Obtener la palabra a buscar.
            palabra = message.content[5:]
            #Resultados en español.
            wikipedia.set_lang("es")
            #Buscar la palabra en wikipedia.
            resultado = wikipedia.summary(palabra, sentences=2)
            #Contestar con el resultado.
            await message.channel.send(resultado)

        #Hacer ping a un host con el comando !ping host
        if message.content.startswith('!ping'):
            #Obtener el host.
            host = message.content[6:]
            #Ejecutar el comando.
            response = subprocess.call(['ping', host])
            #Contestar con el resultado.
            if response == 0:
                await message.channel.send('El host parece estar en linea.')
            else:
                await message.channel.send('Pareceque el host no está en linea.')

        #Contesta con el chat log de la persona con el comando !chatlog.
        if message.content.startswith('!chatlog'):
            #Leer el chat log.
            chat_log = read_chat()
            #Contestar con el chat log.
            await message.channel.send(chat_log)

    #Rececpción de la consulta para GPT-3 y contestación.
    else:
        # solo contestar al 1% de los mensajes que no son del bot.
        if random.randint(1,100) == 1:
            chat_history = read_chat()
            chat_log=session_prompt+chat_history
            answer = ask(message.content, chat_log)
            now = datetime.datetime.now()
            fechalog = (now.strftime("%Y-%m-%d %H:%M:%S"))
            #Si la respuesta está vacía, envía nuevamente la consulta a GPT-3.
            if len(answer) < 1:
                answer = ask(message.content, chat_log)
                print('Reenviando consulta a GPT-3...')
                await message.channel.send(answer)
            await message.channel.send(answer)

#Iniciar el bot.
bot.run(discord_token)
