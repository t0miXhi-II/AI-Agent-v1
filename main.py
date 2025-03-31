# This file is for the main logic of the AI Agent
# The .env file is to hold information such as the API keys

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic



load_dotenv() # Loads the .env file

if __name__=="__main__":
    print("True")
