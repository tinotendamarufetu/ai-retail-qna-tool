import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from your .env file!")

# Initialize Groq client
client = Groq(api_key=api_key)

# Print all active models available to your API key
models = client.models.list()
print("--- Active Groq Models ---")
for model in models.data:
    print(model.id)