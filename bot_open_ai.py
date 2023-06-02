import telebot
import openai
from API_keys import api_key, bot_token


# Configure your OpenAI API credentials
openai.api_key = api_key

# Configure your Telegram bot token
bot_token = bot_token

# Create an instance of the Telegram Bot
bot = telebot.TeleBot(bot_token)

# Handle the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the OpenAI Bot! Type /help to see the available commands.")


# Define a command handler for the /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "You can use the /ask command to ask a question to the OpenAI API.")


# Define a command handler for the /ask command
@bot.message_handler(commands=['ask'])
def send_question(message):
    try:
        # Send a message asking for the user`s question
        bot.reply_to(message, "What`s your question?")
        # Define a function to handle the user`s response

        def handle_question(response):
            try:

                # Call the OpenAI API to get the answer to the question
                result = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=response.text,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.7
                    )
                bot.reply_to(message, response.choices[0].text)
            except Exception as e:
                bot.reply_to(message, "Sorry, I could not get an answer to your question. Please try again later.")
        bot.register_next_step_handler(message, handle_question)

    except Exception as e:
        bot.reply_to(message, "Sorry, I could not get an answer to your question. Please try again later.")

# Start the bot
bot.polling()
