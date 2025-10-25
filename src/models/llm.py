# import libraries
import os
try:
  # optional: load from .env if python-dotenv is available
  from dotenv import load_dotenv
  load_dotenv()
except Exception:
  # if dotenv isn't installed or .env missing, continue; we'll read env vars at runtime
  pass

try:
  from openai import OpenAI
except Exception:
  OpenAI = None

# read token lazily; do not crash at import time if missing
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
 
# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0):
  # Ensure OpenAI client and token are available at call time
  if OpenAI is None:
    raise RuntimeError("OpenAI client library is not installed. Please install the 'openai' package.")

  api_key = os.environ.get("GITHUB_TOKEN") or token
  if not api_key:
    raise RuntimeError("LLM API token not configured. Set GITHUB_TOKEN in environment or .env file.")

  client = OpenAI(base_url=endpoint, api_key=api_key)
  response = client.chat.completions.create(
    messages=messages,
    temperature=temperature, top_p=top_p, model=model)
  return response.choices[0].message.content

# A function to translate test using the LLM model
def translate(text, target_language):
  messages = [
    {"role": "system", "content": "You are a helpful assistant that translates text."},
    {"role": "user", "content": f"Translate the following text to {target_language}:\n\n{text}"}
  ]
  translation = call_llm_model(model, messages)
  return translation

# main function
if __name__ == "__main__":
  text = "Hello, what is your name?"
  target_language = "chinese"
  translated_text = translate(text, target_language)
  print(f"Original Text: {text}")
  print(f"Translated Text: {translated_text}")