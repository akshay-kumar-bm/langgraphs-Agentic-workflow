from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper

from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
import os 
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')


arxiv_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=300)
arxic_tool=ArxivQueryRun(api_wrapper=arxiv_wrapper)
arxic_tool.invoke("Artificial Intelligence")

wikipedia_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=300)
wikipedia_tool=WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

wikipedia_tool.invoke("Akshay Kumar actor ")
tools=[wikipedia_tool,arxic_tool]

from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition

class State(TypedDict):
    messages:Annotated[list,add_messages]

graph_builder=StateGraph(State)


llm=ChatOpenAI(model="gpt-4o-mini")

model_tool=llm.bind_tools(tools=tools)

model_tool.invoke([("user","block chain reserch ")])

def chatbot(state:State):
    return {"messages":model_tool.invoke(state["messages"])}

tool_node=ToolNode(tools=tools)


graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",tool_node)



graph_builder.add_edge(START,"chatbot")


graph_builder.add_conditional_edges("chatbot",tools_condition)
graph_builder.add_edge("tools","chatbot")
graph_builder.add_edge("chatbot",END)

graph_builder=graph_builder.compile()

from IPython.display import display,Image
display(Image(graph_builder.get_graph().draw_mermaid_png()))



graph_builder.invoke({"messages":[("user","Can AI replace AI?")]})


