# This file is for the main logic of the AI Agent
# The .env file is to hold information such as the API keys

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import anthropic
from langchain_core.prompts import ChatPromptTemplate # For prompt template
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool


load_dotenv() # Loads the .env file

class ResearchResponse(BaseModel): # BaseModel is from the 'pydantic' library
    '''This class specifies the type of content that 
        we want our LLM to generate or create.
        This is the format for the output.'''
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    '''The information above specifies all the fields which 
        will serve as output format from our LLM.'''
    

# LLM Choice - There are 2 options, as shown below
llm  = ChatAnthropic(model="claude-3-5-sonnet-20241022") # Don't forget your API key => Get Anthropic API key from: https://console.anthropic.com/settings/keys
# llm_option2  = ChatOpenAI(model="gpt-4o-mini") # if this is chosen, a ChatOpenAI API Key will be needed => get OpenAI API key from: https://platform.openai.com/api-keys


# Output Response Parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse) # ResearchResponse is the template class specified above

# AI Agent prompt - instructions/guide for our AI Agent
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper. 
            Answer the user query and use necessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"), # Note the quary part
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions()) # Our output template from the 'parser' variable is fed as input into the prompt
# The format for the prompt above can be found in the langchain documentation


# Agent creation
tools = [search_tool, wiki_tool, save_tool] # Tools from tools.py (agent can still work without them)
agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools = tools
)

agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True) # Verbose=True -> shows the thinking process of the AI Agent; the value can be set to False to turn it Off.
query = input("Hi, What would you like to know? \n")
raw_response = agent_executor.invoke({"query": query}) # Query from the prompt section above; You can pass muiltiple queries -> e.g. {"query": "What is the capital of Italy?", "name": "Alice"}

# Customising the Agent response presentation
try: 
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response")
    print("Error: ", e)
    print("Raw Response: ", raw_response)



#response = llm.invoke("What is the meaning of invoke?")
#print(f"LLM Response: \n{response}")

