from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.ext import ContextTypes
from telegram import Update

import logging
import yaml

from secrets import OPENROUTER_API_KEY, OPENROUTER_API_BASE, FIRECRAWL_API_KEY
from llm import LanguageModel
from utils import MyFirecrawlApp


# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


llm = LanguageModel(
    model_name="deepseek/deepseek-chat-v3-0324:free",
    temperature=0.0,
    openrouter_api_key=OPENROUTER_API_KEY,
    openrouter_api_base=OPENROUTER_API_BASE,
)


fc_app = MyFirecrawlApp(api_key=FIRECRAWL_API_KEY)


def build_app(token: str):
    app = ApplicationBuilder().token(token).build()
    return app


def set_handlers(app):
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # We can add a default command handler for all messages that are not commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Part 2 - Add a command handler for the /ask command
    app.add_handler(CommandHandler("ask", ask_command))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send the user message back
    """
    await update.message.reply_text(update.message.text)


async def start_command(update: Update, context):
    """
    What to do when the command /start is sent - just a sample text
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I'm your bot. How can I assist you today?",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    What to do when the command /help is sent - show available commands
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id, # means reply to the message
        text="Here are the commands you can use:\n"
             "/start - Start the bot\n"
             "/help - Get help\n"
             "/ask <link> - Ask the LLM about a link"
    )


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    What to do when the command /ask is sent - ask the LLM
    """
    # Get the user input from the message
    link = context.args[0]
    
    if not link:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide a link the /ask command."
        )
        return

    # Scrape the URL using Firecrawl
    try:
        scraped_data = fc_app.scrape_url(link)
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Failed to scrape the URL: {str(e)}"
        )
        return
    
    # Extract the text content from the scraped data
    text_content = scraped_data.markdown

    # Call the LLM with the user input
    prompt = f"Please summarize the following content in a short paragraph:\n\n{text_content}"

    # for this demo, we'll use Paul Graham's latest essay: https://paulgraham.com/do.html

    response = llm(text_content)

    # Send the response back to the user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
    )


def main():
    # Option 1: Load the token from a YAML file
    yaml_file = 'config.yaml'
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    token = config['telegram']['token']

    # Option 2: Load the token from a secrets file
    # from secrets import TELEGRAM_TOKEN
    # token = TELEGRAM_TOKEN

    # Option 3: Load the token from an environment variable
    # token = os.getenv('TELEGRAM_TOKEN')

    # Option 4: Load tokens from a .env file 
    # from dotenv import load_dotenv
    # load_dotenv()
    # token = os.getenv('TELEGRAM_TOKEN')


    app = build_app(token)
    set_handlers(app)

    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == '__main__':
    main()
