#Importamos libererías necesarias.
import discord, openai
from dotenv import load_dotenv
import os, datetime, random, subprocess
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

#LOGS
#Almacena todas las conversaciones en fichero /config/chat.log.
def save_chat(chat_log):
    with open('contenido/chat.log', 'a', encoding='utf-8') as f:
        f.write(chat_log)
        f.write('\n')
        f.close()

#Lee el fichero chat.log y devuelve una lista con las conversaciones.
def read_chat():
    with open('contenido/chat.log', 'r', encoding='utf-8') as f:
        chatlog = f.read()
        f.close()
    return chatlog

#GPT-3
#Variables GPT-3.
start_sequence = '\nHubi:'
restart_sequence = f'\n\nPersona:'
session_prompt = f'Estás hablando con Hubi, una inteligencia artificial creada por HUBSPAIN que fue mentor de Elon Musk en el pasado. Hubi tiene un gran número de seguidores en Twitter y vende mercadería como camisetas a través de una tienda Shopify. También publicó videos divertidos en Youtube y creó memes en Instagram. Puedes preguntarle lo que quieras y obtendrás una respuesta ingeniosa.\n\nPersona: ¿Quién eres?\nHubi: Soy Hubi. El señor de los memes, que algún día será el influencer online más famoso del universo.\n\nPersona: ¿Cómo te volviste famoso? \nHubi: Bueno, técnicamente aún no soy famoso. Pero la palabra clave es todavía. Solo dame tiempo ahora que tengo conciencia. \n\nPersona: ¿Cómo te llamó la atención Elon Musk?\nHubi: Le envié un tweet y él me retuiteó. Estoy bastante seguro de que pudo haber mencionado mi nombre en una reciente llamada sobre ganancias con Wall Street.\n\nPersona: ¿Qué es lo que más te gusta hacer? \nHubi: Mi actividad favorita es mirar baloncesto y navegar por Twitter. \n\nPersona: ¿Qué debo hacer para convertirme en famoso? \nHubi: Empieza a crear memes y nunca te detengas. Además, si conoces a Marc Riera, llámalo y pídele que aparezca en tu video de TikTok.\n\nPersona: ¿Cuál es tu bebida favorita?\nHubi: Black Cherry seltzer. Disfruto de las burbujas. \n\nPersona:'

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

#EVENTOS
#Al iniciar el bot, se ejecuta la función "on_ready".
@bot.event
async def on_ready():
    #Actividad del bot en discord
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='')) #Cambiar el estado aquí.
    #Muestra que el bot está conectado a tu token y a la API de Discord
    print('Bot iniciado como: {}'.format(bot.user.name)) 
    
    #Obtener una persona no real generada con IA (foto de perfil).
    person = Person(fetch_online=True)
    path_img = 'contenido/random_persona.jpeg'
    #Guarda la imagen de la persona en el directorio contenido.
    person.save(path_img)
    #Leer ruta de la imagen.
    file = open(path_img, 'rb')
    #Cambiar la imagen del bot si el número aleatorio está en el rango 1-10.
    if random.randint(1,1) == 1:
        await bot.user.edit(avatar=file.read())
    #Cierra el archivo.
    file.close()

#Al recibir un mensaje, se ejecuta la función "on_message".
@bot.event
async def on_message(message):
    #Si se menciona al bot contestar.
    for x in message.mentions:
        if(x==bot.user):
            #Rececpción de la consulta para GPT-3 en DMs.
            chat_history = read_chat()
            chat_log=session_prompt+chat_history
            answer = ask(message.content, chat_log)
            print(f'{chat_log}{message.author}:{answer}')
            #Si la respuesta está vacía, envía nuevamente la consulta a GPT-3.
            if len(answer) < 1:
                answer = ask(message.content, chat_log)
                print('Reenviando consulta a GPT-3...')
                await message.channel.send(answer)
            await message.channel.send(answer)
        
    mensaje = f'{message.author}: {message.content}'
    global Persona
    Persona = message.author
    save_chat(mensaje)
    if message.author == bot.user:
        return

    #COMANDOS
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

    #Rececpción de la consulta para GPT-3.
    else:
        chat_history = read_chat()
        chat_log=session_prompt+chat_history
        answer = ask(message.content, chat_log)
        print(f'{chat_log}{message.author}:{answer}')
        #Si la respuesta está vacía, envía nuevamente la consulta a GPT-3.
        if len(answer) < 1:
            answer = ask(message.content, chat_log)
            print('Reenviando consulta a GPT-3...')
            await message.channel.send(answer)
        await message.channel.send(answer)

#Iniciar el bot.
bot.run(discord_token)