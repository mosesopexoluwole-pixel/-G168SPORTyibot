import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import BotUtils

class BotHandlers:
    def __init__(self):
        self.utils = BotUtils()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a welcome message when the command /start is issued"""
        user = update.effective_user
        welcome_text = f"""
Welcome {user.first_name} to G168SPORTyibot

I am a privacy-oriented utility bot focused on generating information.
Here are my available commands:

/generate - Show generation options
/help - Show this help message

Click /generate to get started with all available tools.
"""
        await update.message.reply_text(welcome_text)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send detailed help message"""
        help_text = """
G168SPORTyibot - Privacy-Oriented Utility Bot

Available Commands:
/start - Welcome message
/help - Show this help

Generation Commands:
/password [length] [special] - Generate secure password
/username [style] [length] - Generate username
/uuid [version] - Generate UUID
/random [min] [max] - Generate random number
/string [length] [special] - Generate random string
/hash [algorithm] [text] - Generate hash
/base64 [encode/decode] [text] - Base64 operations
/url [encode/decode] [text] - URL operations
/timestamp [format] - Get timestamp

Examples:
/password 20
/password 16 false
/username random
/username simple 12
/uuid 4
/random 1 100
/string 15
/string 10 true
/hash sha256 "Hello World"
/base64 encode "Hello"
/url decode "Hello%20World"
/timestamp iso
"""
        await update.message.reply_text(help_text)

    async def generate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show inline keyboard with all generation options"""
        keyboard = [
            [
                InlineKeyboardButton("Password", callback_data="gen_password"),
                InlineKeyboardButton("Username", callback_data="gen_username"),
            ],
            [
                InlineKeyboardButton("UUID", callback_data="gen_uuid"),
                InlineKeyboardButton("Random Number", callback_data="gen_random"),
            ],
            [
                InlineKeyboardButton("Random String", callback_data="gen_string"),
                InlineKeyboardButton("Hash", callback_data="gen_hash"),
            ],
            [
                InlineKeyboardButton("Base64", callback_data="gen_base64"),
                InlineKeyboardButton("URL", callback_data="gen_url"),
            ],
            [
                InlineKeyboardButton("Timestamp", callback_data="gen_timestamp"),
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Select what you want to generate:",
            reply_markup=reply_markup
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle inline keyboard button presses"""
        query = update.callback_query
        await query.answer()
        
        action = query.data
        
        if action == "gen_password":
            password = self.utils.generate_password()
            await query.edit_message_text(
                f"Generated Secure Password:\n\n`{password}`\n\n"
                "Use /password [length] [true/false] to customize",
                parse_mode='Markdown'
            )
        
        elif action == "gen_username":
            username = self.utils.generate_username()
            await query.edit_message_text(
                f"Generated Username:\n\n`{username}`\n\n"
                "Use /username [style] [length] to customize\n"
                "Styles: random, simple, tech",
                parse_mode='Markdown'
            )
        
        elif action == "gen_uuid":
            uuid_str = self.utils.generate_uuid()
            await query.edit_message_text(
                f"Generated UUID (v4):\n\n`{uuid_str}`\n\n"
                "Use /uuid [1/4] to change version",
                parse_mode='Markdown'
            )
        
        elif action == "gen_random":
            number = self.utils.generate_random_number()
            await query.edit_message_text(
                f"Generated Random Number:\n\n`{number}`\n\n"
                "Use /random [min] [max] to customize",
                parse_mode='Markdown'
            )
        
        elif action == "gen_string":
            string = self.utils.generate_random_string()
            await query.edit_message_text(
                f"Generated Random String:\n\n`{string}`\n\n"
                "Use /string [length] [true/false] to customize",
                parse_mode='Markdown'
            )
        
        elif action == "gen_hash":
            await query.edit_message_text(
                "Please use:\n`/hash [algorithm] [text]`\n\n"
                "Algorithms: md5, sha1, sha256, sha512\n"
                "Example: `/hash sha256 Hello World`",
                parse_mode='Markdown'
            )
        
        elif action == "gen_base64":
            await query.edit_message_text(
                "Please use:\n`/base64 [encode/decode] [text]`\n\n"
                "Example: `/base64 encode Hello`",
                parse_mode='Markdown'
            )
        
        elif action == "gen_url":
            await query.edit_message_text(
                "Please use:\n`/url [encode/decode] [text]`\n\n"
                "Example: `/url encode Hello World`",
                parse_mode='Markdown'
            )
        
        elif action == "gen_timestamp":
            timestamp = self.utils.get_timestamp()
            await query.edit_message_text(
                f"Current Timestamp (Unix):\n\n`{timestamp}`\n\n"
                "Use /timestamp [format] to customize\n"
                "Formats: unix, iso, human, date, time",
                parse_mode='Markdown'
            )

    async def password_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /password command"""
        try:
            args = context.args
            length = 16
            use_special = True
            
            if len(args) > 0:
                length = int(args[0])
            if len(args) > 1:
                use_special = args[1].lower() == 'true'
            
            if length < 8 or length > 64:
                await update.message.reply_text("Password length must be between 8 and 64")
                return
            
            password = self.utils.generate_password(length, use_special)
            special_status = "with" if use_special else "without"
            await update.message.reply_text(
                f"Generated Password ({length} chars, {special_status} special):\n\n`{password}`",
                parse_mode='Markdown'
            )
        except ValueError:
            await update.message.reply_text(
                "Invalid parameters. Use:\n`/password [length] [true/false]`",
                parse_mode='Markdown'
            )

    async def username_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /username command"""
        try:
            args = context.args
            style = 'random'
            length = 8
            
            if len(args) > 0:
                style = args[0]
            if len(args) > 1:
                length = int(args[1])
            
            if style not in ['random', 'simple', 'tech']:
                style = 'random'
            
            username = self.utils.generate_username(style, length)
            await update.message.reply_text(
                f"Generated Username (style: {style}):\n\n`{username}`",
                parse_mode='Markdown'
            )
        except ValueError:
            await update.message.reply_text(
                "Invalid parameters. Use:\n`/username [style] [length]`",
                parse_mode='Markdown'
            )

    async def uuid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /uuid command"""
        version = 4
        if context.args:
            try:
                version = int(context.args[0])
                if version not in [1, 4]:
                    version = 4
            except ValueError:
                pass
        
        uuid_str = self.utils.generate_uuid(version)
        await update.message.reply_text(
            f"Generated UUID (v{version}):\n\n`{uuid_str}`",
            parse_mode='Markdown'
        )

    async def random_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /random command"""
        min_val = 0
        max_val = 100
        
        if context.args:
            try:
                if len(context.args) >= 1:
                    min_val = int(context.args[0])
                if len(context.args) >= 2:
                    max_val = int(context.args[1])
            except ValueError:
                await update.message.reply_text(
                    "Invalid parameters. Use:\n`/random [min] [max]`",
                    parse_mode='Markdown'
                )
                return
        
        if min_val >= max_val:
            await update.message.reply_text("Minimum value must be less than maximum")
            return
        
        number = self.utils.generate_random_number(min_val, max_val)
        await update.message.reply_text(
            f"Generated Random Number:\n\n`{number}`\n(Range: {min_val} to {max_val})",
            parse_mode='Markdown'
        )

    async def string_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /string command"""
        length = 10
        include_special = False
        
        if context.args:
            try:
                if len(context.args) >= 1:
                    length = int(context.args[0])
                if len(context.args) >= 2:
                    include_special = context.args[1].lower() == 'true'
            except ValueError:
                await update.message.reply_text(
                    "Invalid parameters. Use:\n`/string [length] [true/false]`",
                    parse_mode='Markdown'
                )
                return
        
        string = self.utils.generate_random_string(length, include_special)
        special_status = "with" if include_special else "without"
        await update.message.reply_text(
            f"Generated Random String ({length} chars, {special_status} special):\n\n`{string}`",
            parse_mode='Markdown'
        )

    async def hash_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /hash command"""
        try:
            args = context.args
            if len(args) < 2:
                await update.message.reply_text(
                    "Usage:\n`/hash [algorithm] [text]`\n\n"
                    "Algorithms: md5, sha1, sha256, sha512",
                    parse_mode='Markdown'
                )
                return
            
            algorithm = args[0]
            text = ' '.join(args[1:])
            
            hash_result = self.utils.generate_hash(text, algorithm)
            await update.message.reply_text(
                f"Hash ({algorithm}):\n\n`{hash_result}`\n\nText: `{text}`",
                parse_mode='Markdown'
            )
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def base64_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /base64 command"""
        try:
            args = context.args
            if len(args) < 2:
                await update.message.reply_text(
                    "Usage:\n`/base64 [encode/decode] [text]`",
                    parse_mode='Markdown'
                )
                return
            
            operation = args[0].lower()
            text = ' '.join(args[1:])
            
            if operation == 'encode':
                result = self.utils.base64_encode(text)
                await update.message.reply_text(
                    f"Base64 Encoded:\n\n`{result}`\n\nOriginal: `{text}`",
                    parse_mode='Markdown'
                )
            elif operation == 'decode':
                result = self.utils.base64_decode(text)
                if result is None:
                    await update.message.reply_text("Invalid Base64 string")
                else:
                    await update.message.reply_text(
                        f"Base64 Decoded:\n\n`{result}`\n\nOriginal: `{text}`",
                        parse_mode='Markdown'
                    )
            else:
                await update.message.reply_text(
                    "Invalid operation. Use 'encode' or 'decode'"
                )
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def url_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /url command"""
        try:
            args = context.args
            if len(args) < 2:
                await update.message.reply_text(
                    "Usage:\n`/url [encode/decode] [text]`",
                    parse_mode='Markdown'
                )
                return
            
            operation = args[0].lower()
            text = ' '.join(args[1:])
            
            if operation == 'encode':
                result = self.utils.url_encode(text)
                await update.message.reply_text(
                    f"URL Encoded:\n\n`{result}`\n\nOriginal: `{text}`",
                    parse_mode='Markdown'
                )
            elif operation == 'decode':
                result = self.utils.url_decode(text)
                if result is None:
                    await update.message.reply_text("Invalid URL encoded string")
                else:
                    await update.message.reply_text(
                        f"URL Decoded:\n\n`{result}`\n\nOriginal: `{text}`",
                        parse_mode='Markdown'
                    )
            else:
                await update.message.reply_text(
                    "Invalid operation. Use 'encode' or 'decode'"
                )
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def timestamp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /timestamp command"""
        format_type = 'unix'
        if context.args:
            format_type = context.args[0].lower()
        
        timestamp = self.utils.get_timestamp(format_type)
        await update.message.reply_text(
            f"Current Timestamp ({format_type}):\n\n`{timestamp}`",
            parse_mode='Markdown'
        )
