"""
A simple chatbot that integrates the OpenAI's ChatGPT API.
"""

import pathlib
import tomllib
import asyncio

import openai
from telebot.async_telebot import AsyncTeleBot


confpath = pathlib.Path(__file__).parent / 'config.toml'
with confpath.open(mode='rb') as cf:
    config = tomllib.load(cf)

bot = AsyncTeleBot(config['TELEGRAM_TOKEN'], parse_mode='MARKDOWN')
openai.api_key = config['OPENAI_API_KEY']

history = {}    
messages = []   

if len(config['openai']['context']) > 0:
    messages.append({'role': 'system', 'content': config['openai']['context']})


def debug(str):
    print(str) if config['debug'] else None


@bot.message_handler(commands=['restart'])
async def erase_history(message):
    chat_id = message.chat.id
    if not config['keep_history']:
        info = '_Chat history is disabled._'
    elif chat_id in history.keys():
        del history[chat_id][1:]
        info = '_Chat history has been cleared._'
    else:
        info = '_Chat history is empty._'
    await bot.reply_to(message, info)


@bot.message_handler(commands=['system'])
async def add_context(message):
    context = message.text.removeprefix('/system').lstrip()
    if len(context) > 0:
        debug(f'=> New instruction: {context}')
        messages.append({'role': 'system', 'content': context})


@bot.message_handler(content_types=['text'])
async def chatbot_reply(message):
    chat_id, username = message.chat.id, message.from_user.first_name
    print(f'=> {username.capitalize()}: {message.text}')
    try:
        answer = await create_prompt(chat_id, message.text)
        await bot.send_message(chat_id, answer)
    except Exception as e:
        print(f'=> Chatbot failed to aswer: {e}')


def format_messages(chat_id, msg):
    message = {'role': 'user', 'content': msg}
    if config['keep_history']:
        history.setdefault(chat_id, messages)
        history[chat_id].append(message)
        debug(f'=> Chat history:\n{history[chat_id]}')
        return history[chat_id]

    messages.append(message)
    debug(f'=> Messages:\n{messages}')
    return messages


async def create_prompt(chat_id, input):
    params = config['openai']
    output = openai.ChatCompletion.create(
        model=params['model'],
        temperature=params['temperature'],
        max_tokens=params['max_tokens'],
        top_p=params['top_p'],
        frequency_penalty=params['frequency_penalty'],
        presence_penalty=params['presence_penalty'],
        messages=format_messages(chat_id, input)
    )
    completion = output.choices[0].message.content

    if config['keep_history']:
        history[chat_id].append({'role': 'assistant', 'content': completion})

    debug(f'=> OpenAI output: {output}')
    print(f'=> Chatbot: {completion}')

    return completion


async def main():
    try:
        print('=> Chatbot is running')
        await bot.infinity_polling(timeout=90)
    except Exception as e:
        print(f'=> Chatbot failed to start: {e}')


if __name__ == '__main__':
    asyncio.run(main())
