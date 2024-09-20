import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram
TELEGRAM_API_KEY    = os.getenv('TELEGRAM_API_KEY')
TELEGRAM_IDS        = {
    'TEST': os.getenv('TEST_ID'),
    'MOGAIKA': os.getenv('MOGAIKA_ID'),
    'POLYA': os.getenv('POLYA_ID'),
    'YASHA': os.getenv('YASHA_ID'),
    'LENA': os.getenv('LENA_ID'),
    'GRISHA': os.getenv('GRISHA_ID'),
}

# Weatherapi
WEATHERAPI_API_KEY  = os.getenv('WEATHERAPI_API_KEY')
WEATHERAPI_URL      = f'http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_API_KEY}&q=Moscow&aqi=no'

# Mistral
MISTRAL_API_KEY     = os.getenv('MISTRAL_API_KEY')
MISTRAL_URL         = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODELS      = {
    'SMALL': "mistral-small-latest",
    'MEDIUM': "mistral-medium-latest",
    'LARGE': "mistral-large-latest",
    'XL': "mistral-xl-latest",
    'MULTILINGUAL': "mistral-multilingual-latest",
    'SUMMARIZATION': "mistral-summarization-latest",
    'CODE': "mistral-code-latest",
    'QA': "mistral-qa-latest",
}

JSON_DATA = 'data/users.json'
JSON_CALENDAR = 'data/calendar.json'
WEEKS = 4