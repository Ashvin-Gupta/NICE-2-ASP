import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = {
    'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY', ''),
}
