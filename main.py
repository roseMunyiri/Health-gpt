import os
from os.path import abspath
from dotenv import load_dotenv
import openai
import telebot

basedir = abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

Bot_Token = os.getenv('Bot_Token')
openai.api_key = os.getenv('Api_Key')


bot = telebot.TeleBot(Bot_Token)

@bot.message_handler(commands=['start'])
def start(message):
    """
    Function that starts the bot
    """
    # Check username
    username = message.from_user.username

    if username:
        personalized_greeting = f'Hello there {username}!'
    else:
        personalized_greeting = "Hello there!"

    # Read the contents of start.txt
    start_text = ""
    try:
        with open("messages/start.txt", "r") as file:
            start_text = file.read()
    except FileNotFoundError:
        start_text = "Welcome! I'm here to assist you with your health-related questions."

    # Combine the personalized greeting and the contents of start.txt
    welcome_message = f"{personalized_greeting}\n\n{start_text}"

    # Send the welcome message
    bot.send_message(message.chat.id, text=welcome_message)

@bot.message_handler(commands=['help'])
def help(message):
    # Read the contents of help.txt
    help_text = ""
    try:
        with open("messages/help.txt", "r") as file:
            help_text = file.read()
    except FileNotFoundError:
        help_text = "Welcome! I'm here to assist you with your health-related questions."

    # Send the help message
    bot.send_message(message.chat.id, text=help_text)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """
    A function that handles all incoming messages
    """
    # Read the prompt
    prompt = ""
    try:
        with open("messages/prompt.txt", "r") as file:
            prompt = file.read()
    except FileNotFoundError:
        prompt = "Sorry, this file is currently unavailable"

    user_input = message.text

    # Check if the user input is empty or contains only whitespace
    if not user_input or user_input.strip() == "":
        bot.send_message(message.chat.id, "Please provide a valid message.")
        return

    # Call OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5
    )

    # Extract the response from OpenAI
    bot_response = response.choices[0].message["content"]

    # Send the response to the user
    bot.send_message(message.chat.id, bot_response)

@bot.message_handler(commands=['stop'])
def stop(message):
    """
    Function to end the conversation
    """

    # Read stop text
    stop_text = ""
    try:
        with open("messages/stop.txt", "r") as file:
            stop_text = file.read()
    except FileNotFoundError:
        stop_text = "Thank you for using nuttri-bot, your personal health assistant"

    # Send message
    bot.send_message(message.chat.id, text=stop_text)

try:
    bot.polling()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    bot.stop_polling()
