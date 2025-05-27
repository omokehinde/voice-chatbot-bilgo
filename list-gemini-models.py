# This script lits out available Gemini models using the Google Generative AI library.
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure your Google API key is set in your .env file as GOOGLE_API_KEY
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("Listing available Gemini models:")
    for m in genai.list_models():
        # Filter for models that support 'generateContent' as they are typically chat models
        if "generateContent" in m.supported_generation_methods:
            print(f"  Model Name: {m.name}")
            print(f"    Description: {m.description}")
            print(f"    Input Token Limit: {m.input_token_limit}")
            print(f"    Output Token Limit: {m.output_token_limit}")
            print(f"    Supported Methods: {m.supported_generation_methods}")
            print("-" * 30)
else:
    print("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")