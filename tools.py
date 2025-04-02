# This file for for storing the tools the AI Agent will be using
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime


# Custom Tool - The tool saves the 
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)

    return f"Data successfully saved to {filename}"


# Wrap/package our above function as a tool -> name: save_tool
save_tool = Tool(   
    name = "save_text_to_file", # Any name can be used here (name MUST NOT have any spaces)
    func = save_to_txt, # The function the tool will be providing
    description = "Save structured research data to a text file",
) 

# DuckDuckGoSearchRun Tool -> name: search_tool
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name = "search", # Any name can be used here (name MUST NOT have any spaces)
    func = search.run, # The function the tool will be providing
    description = "Search the web for information",
)

# Wikipedia Tool -> name: wiki_tool
api_wrapper = WikipediaAPIWrapper(top_k_results = 1, doc_content_chars_max = 120)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


