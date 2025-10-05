""" API anahtarlarını .env dosyasından yükler ve global değişkenler olarak hazırlar. """

import os
from dotenv import load_dotenv

load_dotenv()

exchange_rate_api_key = os.getenv("EXCHANGE_RATE_API")

finn_api_key = os.getenv("FINNHUB_API_KEY")
