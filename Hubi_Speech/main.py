# HUBI.AI Speech 1.0 - Main
# Hubi Speech is a gpt-3 chatbot
# OpenAI GPT-3 is a generative model for text generation
# Recognizes speech to text and text to speech

from time import sleep
from config.settings import gpt3_api_token, default_language, bot_name, human_name, context
from config.functions.voice_tools import recognition_listen, recognition_results, microphone, speak
from config.functions.gpt3 import send_prompt_gpt3

#Start the conversation
if __name__ == "__main__":
    while True:
        try:
            #Record user's voice
            with microphone as source:
                #Listen user's voice
                sleep(1)
                print ("Listening...")
                audio = recognition_listen(source)
                #Recognize speech
                text = recognition_results(audio, language=default_language)
                print ("You said:", text)
                # if text contains the word 'exit', break the loop
                if 'exit' in text:
                    print('Closing program...Bye!')
                    break
                #Send text to openai gpt-3
                response = send_prompt_gpt3(gpt3_api_token, human_name, bot_name, context, text)
                #Speak response
                speak(response)
        except KeyboardInterrupt:
            print('\n\nClosing program...Bye!')
            break
        except Exception as e:
            print(e)
            print('Something went wrong... Please try again...\n')
            sleep(1)
            continue
