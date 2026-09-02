import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
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

def main():
    """Start the bot"""
    # Get bot token from environment
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        logger.error("BOT_TOKEN not found in environment variables")
        return
    
    logger.info("Starting G168SPORTyibot...")
    
    try:
        # Create application
        application = Application.builder().token(bot_token).build()
        
        # Initialize handlers
        handlers = BotHandlers()
        
        # Add command handlers
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
        
        # Add callback handler for inline buttons
        application.add_handler(CallbackQueryHandler(handlers.button_callback))
        
        # Start polling
        logger.info("Bot is running with polling mode...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()
