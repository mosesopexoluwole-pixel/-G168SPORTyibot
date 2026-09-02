import secrets
import string
import hashlib
import base64
import urllib.parse
import uuid
import time
from datetime import datetime
from typing import Optional

class BotUtils:
    @staticmethod
    def generate_password(length: int = 16, use_special: bool = True) -> str:
        """Generate a secure random password"""
        if length < 8:
            length = 8
        if length > 64:
            length = 64
            
        chars = string.ascii_letters + string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password

    @staticmethod
    def generate_username(style: str = 'random', length: int = 8) -> str:
        """Generate random username with different styles"""
        adjectives = ['Cool', 'Happy', 'Smart', 'Swift', 'Brave', 'Wise', 'Lucky', 'Noble', 'Epic', 'Mighty']
        nouns = ['Tiger', 'Eagle', 'Dragon', 'Wolf', 'Phoenix', 'Lion', 'Shark', 'Hawk', 'Falcon', 'Python']
        
        if style == 'random':
            adj = secrets.choice(adjectives)
            noun = secrets.choice(nouns)
            number = secrets.randbelow(1000)
            return f"{adj}{noun}{number}"
        elif style == 'simple':
            if length < 4:
                length = 4
            if length > 20:
                length = 20
            chars = string.ascii_lowercase + string.digits
            return ''.join(secrets.choice(chars) for _ in range(length))
        elif style == 'tech':
            prefixes = ['dev', 'tech', 'code', 'byte', 'data', 'cyber', 'sys', 'net']
            suffix = secrets.token_hex(length // 2)
            return f"{secrets.choice(prefixes)}_{suffix}"
        else:
            # Default to random style
            adj = secrets.choice(adjectives)
            noun = secrets.choice(nouns)
            number = secrets.randbelow(100)
            return f"{adj}{noun}{number}"

    @staticmethod
    def generate_uuid(version: int = 4) -> str:
        """Generate UUID (version 1 or 4)"""
        if version == 1:
            return str(uuid.uuid1())
        else:
            return str(uuid.uuid4())

    @staticmethod
    def generate_random_number(min_val: int = 0, max_val: int = 100) -> int:
        """Generate random number between min and max"""
        if min_val >= max_val:
            min_val, max_val = 0, 100
        return secrets.randbelow(max_val - min_val + 1) + min_val

    @staticmethod
    def generate_random_string(length: int = 10, include_special: bool = False) -> str:
        """Generate random string"""
        if length < 1:
            length = 1
        if length > 50:
            length = 50
            
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*"
        return ''.join(secrets.choice(chars) for _ in range(length))

    @staticmethod
    def generate_hash(text: str, algorithm: str = 'sha256') -> str:
        """Generate hash of text using specified algorithm"""
        hash_functions = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
        
        if algorithm.lower() not in hash_functions:
            algorithm = 'sha256'
        
        hash_obj = hash_functions[algorithm.lower()]()
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()

    @staticmethod
    def base64_encode(text: str) -> str:
        """Encode text to Base64"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base64_decode(encoded: str) -> Optional[str]:
        """Decode Base64 to text"""
        try:
            return base64.b64decode(encoded).decode('utf-8')
        except Exception:
            return None

    @staticmethod
    def url_encode(text: str) -> str:
        """URL encode text"""
        return urllib.parse.quote(text, safe='')

    @staticmethod
    def url_decode(encoded: str) -> Optional[str]:
        """URL decode text"""
        try:
            return urllib.parse.unquote(encoded)
        except Exception:
            return None

    @staticmethod
    def get_timestamp(format_type: str = 'unix') -> str:
        """Get current timestamp in various formats"""
        current_time = datetime.now()
        
        formats = {
            'unix': str(int(time.time())),
            'iso': current_time.isoformat(),
            'human': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'date': current_time.strftime('%Y-%m-%d'),
            'time': current_time.strftime('%H:%M:%S'),
            'full': current_time.strftime('%A, %B %d, %Y at %I:%M:%S %p')
        }
        
        return formats.get(format_type.lower(), formats['unix'])
