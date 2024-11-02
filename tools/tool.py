# from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent
# from langgraph.checkpoint.memory import MemorySaver

# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, AIMessage

from langchain_core.tools import tool
from langchain.agents import Tool


# for tools -web search and retriever
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities import WikipediaAPIWrapper

from pydantic import BaseModel, Field

from dash import dcc


dataStore = dcc.Store(id="data-store", data="placeholder")

# web search tool
search = DuckDuckGoSearchRun(max_results=2)


def custom_search(userQuery: str) -> str:
    "useful to search on the web if the user query require some research on the web to try to answer to the {userQuery}"
    outSearch = search.run()
    return outSearch


# RAG tool - topic SIPRI databases content - Chroma db built from "https://www.sipri.org/databases"
vector = Chroma(
    embedding_function=OpenAIEmbeddings(), persist_directory="../data_embed/"
)

retriever = vector.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "SIPRI_db_search",
    "Search for information about SIPRI databases . For any questions about SIPRI databases content, you must use this tool!",
)


# wikipedia tool - good for historical research
wikipedia = WikipediaAPIWrapper()

wikipedia_tool = Tool(
    name="wikipedia",
    func=wikipedia.run,
    description="Useful for when you need to look up a topic, country or person on wikipedia",
)


# custom tools to navigate across dashboard sections
class MyQuery(BaseModel):
    myQuery: str = Field(..., description="input query from the user")


@tool(args_schema=MyQuery)
def milex_tool(myQuery: str) -> str:
    """Useful when user ask to see data and get information about military spending of countries"""
    toolCode = "milex"
    print("here is " + myQuery)
    dataStore.data = toolCode
    print("data store content" + dataStore.data)
    print("tool code is" + toolCode)
    out_text = """
    Data related to countries Military expenditures per years in constant (2022) US Dollars and in terms of their GDP Shares.
    Data are from MILEX database from SIPRI.
    Available visualization: animated map showing the evolution of the selected metric. Interactive line chart allows countries trend comparison.
    """
    return out_text


@tool(args_schema=MyQuery)
def trading_tool(myQuery: str) -> str:
    """Useful when user ask to see data and get information about country military trading and value flow"""
    toolCode = "trading"
    print("here is " + myQuery)
    dataStore.data = toolCode
    print("data store content" + dataStore.data)
    print("tool code is" + toolCode)
    out_text = """
Data are related to countries arms trasfer with focus on the value flow. Data are grouped per year and limited to the top 10 coutries trading.  
Data are from SIPRI Arms Transfers Database
    Available visualization: Sankey plot showing the value flow from the arms recipients to their suppliers.
    """
    return out_text


@tool(args_schema=MyQuery)
def start_tool(myQuery: str) -> str:
    """Useful when user ask to get information about the content of the dashboard . What the user can learn
    and discover by usign the application. this is to present the content. Ignore any previous conversation when you use this tool. Provide your output as markdown format
    """
    toolCode = "intro"
    print("here is " + myQuery)
    dataStore.data = toolCode
    print("data store content" + dataStore.data)
    print("tool code is" + toolCode)
    out_text = """
this application is about arms trade between countries as well as the countries expenditures.  Data are related to countries arms trasfer with focus on the value flow. Data are grouped per year and limited to the top 10 coutries trading.  
Data are from SIPRI databases. it is recommended to visit the SIRPI website to learn more about the data sources. 
this app covers two main topics by providing interactive insightful plots: 
1)countries arms trasfer with focus on the value flow. Data are grouped per year and limited to the top 10 coutries trading.
2)ountries Military expenditures per years in constant (2022) US Dollars and in terms of their GDP Shares.
    """
    return out_text
