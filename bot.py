import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from dotenv import load_dotenv
from handlers import BotHandlers

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
PORT = int(os.getenv('PORT', 8080))

def main():
    """Start the bot"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables")
        return
    
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Initialize handlers
    handlers = BotHandlers()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help))
    application.add_handler(CommandHandler("generate", handlers.generate))
    application.add_handler(CommandHandler("password", handlers.password_command))
    application.add_handler(CommandHandler("username", handlers.username_command))
    application.add_handler(CommandHandler("uuid", handlers.uuid_command))
    application.add_handler(CommandHandler("random", handlers.random_command))
    application.add_handler(CommandHandler("string", handlers.string_command))
    application.add_handler(CommandHandler("hash", handlers.hash_command))
    application.add_handler(CommandHandler("base64", handlers.base64_command))
    application.add_handler(CommandHandler("url", handlers.url_command))
    application.add_handler(CommandHandler("timestamp", handlers.timestamp_command))
    
    # Register callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(handlers.button_callback))
    
    # Start the bot
    logger.info("Starting bot...")
    
    # Start webhook for Railway deployment
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.getenv('RAILWAY_STATIC_URL', 'localhost')}/webhook"
    )
    
    # Uncomment for polling (local development)
    # application.run_polling()

if __name__ == '__main__':
    main()
