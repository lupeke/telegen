"""
A simple Telegram chatbot that integrates the OpenAI's ChatGPT API.
"""

import os
import logging
import asyncio

import openai
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

from config import cfg

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='[CHATBOT] %(levelname)s: %(asctime)s => %(message)s',
    datefmt='%m/%d/%Y @ %I:%M%p')

# Load env vars, create bot instance, etc
load_dotenv()
bot = AsyncTeleBot(os.environ['TELEGRAM_TOKEN'], parse_mode='MARKDOWN')
openai.api_key = os.environ['OPENAI_API_KEY']

# Create basic structures for chat history and prompt messages
history = {}
messages = []


def set_context():
    if len(cfg['openai']['context']) > 0:
        messages.append({'role': 'system',
                         'content': cfg['openai']['context']})


# Give an initial context to the assistant if available
set_context()


# Handle chat history for each user
@bot.message_handler(commands=['restart'])
async def erase_history(message):
    chat_id = message.chat.id
    if not cfg['keep_history']:
        info = '_Chat history is disabled._'
    elif chat_id in history.keys():
        del history[chat_id][:]
        set_context()  # Don't loose initial context
        info = '_Chat history has been cleared._'
    else:
        info = '_Chat history is empty._'
    print(history)
    await bot.reply_to(message, info)


# Give new instruction to the assistant
@bot.message_handler(commands=['system'])
async def add_context(message):
    context = message.text.removeprefix('/system').lstrip()
    if len(context) > 0:
        messages.append({'role': 'system', 'content': context})
        logging.info(f'New instruction: {context}')


# Generate chatbot response
@bot.message_handler(content_types=['text'])
async def reply(message):
    chat_id, username = message.chat.id, message.from_user.first_name
    logging.info(f'{username.capitalize()}: {message.text}')
    try:
        answer = await prompt(chat_id, message.text)
        await bot.send_message(chat_id, answer)
    except Exception as e:
        logging.error(f'Chatbot failed to aswer: {e}')


def format_messages(chat_id, msg):
    message = {'role': 'user', 'content': msg}
    if cfg['keep_history']:
        history.setdefault(chat_id, messages)
        history[chat_id].append(message)
        return history[chat_id]

    messages.append(message)
    return messages


# Get AI's chat completion
async def prompt(chat_id, input):
    params = cfg['openai']
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

    if cfg['keep_history']:
        history[chat_id].append({'role': 'assistant', 'content': completion})

    logging.info(f'Chatbot: {completion}')

    return completion


# Start chatbot
async def main():
    try:
        logging.info('Chatbot is running')
        await bot.infinity_polling(timeout=90, logger_level=None)
    except Exception as e:
        logging.error(f'Chatbot failed to start: {e}')


if __name__ == '__main__':
    asyncio.run(main())
