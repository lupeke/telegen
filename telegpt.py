"""
telegpt is a simple chatbot that integrates the OpenAI's ChatGPT API
to provide an AI powered chat experience on Telegram.
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


def debug(str):
    print(str) if config['debug'] else None


@bot.message_handler(commands=['restart'])
async def erase_history(message):
    chat_id = message.chat.id
    if not config['keep_history']:
        await bot.reply_to(message, '_Chat history is disabled._')
    elif chat_id in history.keys():
        del history[chat_id]
        await bot.reply_to(message, '_Chat history has been cleared._')
    else:
        await bot.reply_to(message, '_Chat history is empty._')


@bot.message_handler(func=lambda msg: True)
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
        history.setdefault(chat_id, [])
        history[chat_id].append(message)
        debug(f'=> Chat history:\n{history[chat_id]}')
        return history[chat_id]

    messages = [message]
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
    print(f'=> Assistant: {completion}')

    return completion


async def main():
    try:
        print('=> Chatbot is running')
        await bot.infinity_polling(timeout=90)
    except Exception as e:
        print(f"=> Can't start chatbot: {e}")


if __name__ == '__main__':
    asyncio.run(main())
