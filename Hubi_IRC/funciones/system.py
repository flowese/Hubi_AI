from os import system, name

# Limpiar terminal.
def limpiar_terminal():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# Directorio de ayuda.
def help():
    ayuda = open('config/ayuda.help','r', encoding='utf-8')
    content = ayuda.read()
    return content