import openai

#Function to send prompt to openai gpt-3
def send_prompt_gpt3(gpt3_api_token ,human_name, bot_name, context, prompt):
    #Read GPT-3 API key
    openai.api_key = gpt3_api_token
    #Start/Stop sequence
    start_sequence = f"\n{bot_name}:"
    restart_sequence = f"\n\n{human_name}:"
    #Read chatlog file if exists
    try:
        with open('logs/chatlog.txt', 'r', encoding="utf-8") as chatlog:
            chatlog = chatlog.read()
    except:
        chatlog = ''
    chat = f'{context} {chatlog} {restart_sequence} {prompt}{start_sequence}'
    #Query openai gpt-3
    response = openai.Completion.create(
        engine="davinci",
        prompt=chat,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
        )
    response = response.choices[0].text

    #append chatlog with utf-8 encoding
    with open('logs/chatlog.txt', 'a', encoding="utf-8") as chatlog:
        chatlog.write(f'{human_name}: {prompt}\n{bot_name}:{response}\n\n')
        #Close chatlog file
        chatlog.close()
    return response