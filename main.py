import dotenv
import os
import requests

#import class
from app.api_structures import APIStructure

dotenv.load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

if not api_key:
    raise ValueError("API_KEY environment variable not set")

api_instance = APIStructure(api_key)
app = api_instance.app
