# HUBI SERVER IA
# Creado por @flowese
# Powered by @hubspain
# Versión Telegram.

# Librerías.
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import json, os, string, sys, threading, logging, time, re, random
import openai


#Ajustes

#OpenAI API key
openai.api_key = "<API_HERE>"
#Telegram bot key
tgkey = "<TOKEN_HERE>"

# Mostrar todo por consola.
debug = True
# TimeOut de la sesión.
timstart = 100

#Valores por defecto.
user = ""
running = False
cache = None
qcache = None
chat_log = None

f1 = open (f'Hubi_Telegram/memoria/hubi_mem/memoria_corta.data','r')
start_chat_log = f1.read()

# Habilitar logging.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

completion = openai.Completion()

# Gestión de hora y fecha.
def reloj_sistema():
    now = datetime.now()
    hora = (now.strftime("%H:%M"))
    fecha = (now.strftime("%D/%M/%Y"))
    return fecha, hora

# Comandos principales.
def start(bot, update):
    # Comando /start.
    global user
    global chat_log
    global qcache
    global cache
    global tim
    fecha, hora = reloj_sistema()
    if user == "":
        user = update.message.from_user.id
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text(f'Estás hablando con Hubi. Son las {hora}.')
        return
    if user == update.message.from_user.id:
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text(f'Actualmente hablando con Hubi. Son las {hora}.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Hubi está actualmente en uso, asegúrese de establecer su configuración cuando se agote el temporizador.' + left + ' segundos.')

def help(bot, update):
    # Comando /help.
    update.message.reply_text('/reset restablece la memoria de Hubi, /retry reenvía el último mensaje a Hubi.')

def reset(bot, update):
    # Comando /reset (memoria de hubi).
    global user
    global chat_log
    global cache
    global qcache
    global tim
    fecha, hora = reloj_sistema()
    if user == "":
        user = update.message.from_user.id
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text(f'SERVIDOR: Se ha restablecido la memoria de Hubi a las {hora}.')
        return
    if user == update.message.from_user.id:
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text(f'SERVER: Memoria de Hubi restablecida a las {hora}.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Hubi está actualmente en uso, asegúrese de establecer su configuración cuando se agote el temporizador.' + left + ' segundos.')

def retry(bot, update):
    #Comando /retry (reenviar ultima respuesta).
    new = True
    comput = threading.Thread(target=wait, args=(bot, update, new,))
    comput.start()

def runn(bot, update):
    # Respuesta de Hubi GPT-3.
    new = False
    comput = threading.Thread(target=wait, args=(bot, update, new,))
    comput.start()


# TimeOut de sesión por usuario.
def wait(bot, update, new):
    global user
    global chat_log
    global cache
    global qcache
    global tim
    global running
    fecha, hora = reloj_sistema()
    if user == "":
        user = update.message.from_user.id
    if user == update.message.from_user.id:
        user = update.message.from_user.id
        tim = timstart
        compute = threading.Thread(target=interact, args=(bot, update, new,))
        compute.start()
        if running == False:
            while tim > 1:
                running = True
                time.sleep(1)
                tim = tim - 1
            if running == True:
                chat_log = None
                cache = None
                qcache = None
                user = ""
                # Devolvemos mensaje de sistema por telegram.
                #update.message.reply_text(f'La sesión ha caducado. Memoria de Hubi reiniciada a las {hora}.')
                running = False
    else:
        left = str(tim)
        update.message.reply_text('Hubi está en uso, la cuenta atrás actuañ es: ' + left + ' segundos.')

# Funciones principales.

# Secuencias de inicio y reinicio para GPT-3.
nombre_persona = 'Persona'
start_sequence = "\nHubi:"
restart_sequence = f"\n\n{nombre_persona}:"

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = completion.create(
        prompt=prompt, 
        engine="davinci", 
        stop=['\n'], 
        temperature=0.7,
        top_p=1, 
        frequency_penalty=0, 
        presence_penalty=0.3,
        max_tokens=90)
    answer = response.choices[0].text.strip()
    return answer

# Insertar chatlogs.
def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Persona: {question}\nHubi: {answer}\n'

# Análisis de sentimientos	
def interact(bot, update, new):
    global chat_log
    global cache
    global qcache
    print("==========Hubi==========")
    tex = update.message.text
    text = str(tex)
    analyzer = SentimentIntensityAnalyzer()
    if new != True:
        vs = analyzer.polarity_scores(text)
        if debug == True:
            print("Análisis de sentimiento:\n")
            print(vs)
            # Fijar a 0 para análisis de sentimientos.
        if vs['neg'] > 1:
            update.message.reply_text('El texto de entrada no es positivo. El texto de entrada debe ser de sentimiento / emoción positiva.')
            return
    if new == True:
        if debug == True:
            print("Chat_LOG Cache es...")
            print(cache)
            print("Question Cache es...")
            print(qcache)
        chat_log = cache
        question = qcache
    if new != True:
        question = text
        qcache = question
        cache = chat_log
    # Devolvemos mensaje de sistema por telegram.  
    #update.message.reply_text('Procesando...')
    try:
        answer = ask(question, chat_log)
        if debug == True:
            print("Persona:\n" + question)
            print("Hubi:\n" + answer)
            print("====================")
        stripes = answer.encode(encoding=sys.stdout.encoding,errors='ignore')
        decoded	= stripes.decode("utf-8")
        out = str(decoded)
        vs = analyzer.polarity_scores(out)
        if debug == True:
            print("Análisis de sentimiento:\n")
            print(vs)
            # Fijar a 0 para análisis de sentimientos.
        if vs['neg'] > 1:
            update.message.reply_text('El texto de salida no es positivo. Censura Activada. Utiliza /retry para obtener un resultado positivo.')
            return
        update.message.reply_text(out)
        chat_log = append_interaction_to_chat_log(question, answer, chat_log)
    except Exception as e:
            print(e)
            errstr = str(e)
            update.message.reply_text(errstr)


## Inicio de APP HUBI.

def error(bot, update):
    # Logs de error.
    logger.warning('La actualización "%s" ha causado el error "%s"', update)

def main():
    # Inicio de Hubi.
    # Creamos declaramos updater.
    # Establecer use_context = True para utilizar llamadas de contexto.
    updater = Updater(tgkey, use_context=False)
    # Crear el dispacher para el updater.
    dp = updater.dispatcher
    # Comandos que acepta Hubi en Telegram.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("retry", retry))
    # Retornar mensaje a telegram.
    dp.add_handler(MessageHandler(Filters.text, runn))
    # Registrar todos los errores en logs.
    dp.add_error_handler(error)
    # Iniciar Hubi.
    updater.start_polling()
     # Ejecutará el bot hasta que se presione Ctrl-C o el proceso reciba SIGINT,
     # SIGTERM o SIGABRT. Esto debe usarse la mayor parte del tiempo, ya que
     # start_polling () debe detener todos los procesos de Hubi correctamente.
    updater.idle()

if __name__ == '__main__':
    main()