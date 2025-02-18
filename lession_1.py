import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')
from langchain_openai import ChatOpenAI
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY="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"
LANGSMITH_PROJECT="langgraph Project"

llm=ChatOpenAI(model="gpt-4o-mini")

# start buildinf chatbot using langgraph

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages

class State(TypedDict):
    message:Annotated[list,add_messages]

graph_builder=StateGraph(State)

def chatbot(state:State):
    user_massge=state["message"]
    respone=llm.invoke(user_massge)
    return {"message":respone}

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

graph=graph_builder.compile()

from IPython.display import display,Image
display(Image(graph.get_graph().draw_mermaid_png()))


result=graph.invoke({"message":"what is ai ,?"})

result["message"][-1].content



