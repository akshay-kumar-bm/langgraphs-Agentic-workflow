from typing import Annotated, TypedDict
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Initialize API wrappers and tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=300)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

tools = [wikipedia_tool, arxiv_tool]

# Define state type
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize graph and LLM
graph = StateGraph(State)
llm = ChatOpenAI(model="gpt-4o-mini")
model_with_tools = llm.bind_tools(tools=tools)

# Define chatbot function
def chatbot(state: State):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": messages + [response]}

# Create tool node
tool_node = ToolNode(tools=tools)

# Add nodes
graph.add_node("chatbot", chatbot)
graph.add_node("tools", tool_node)

# Add edges with proper conditional routing
graph.add_edge(START, "chatbot")

def router(state):
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check if the last message has tool calls
    if hasattr(last_message, 'additional_kwargs') and \
       'tool_calls' in last_message.additional_kwargs and \
       last_message.additional_kwargs['tool_calls']:
        return "tools"
    return "end"

# Add conditional edges with custom router
graph.add_conditional_edges(
    "chatbot",
    router,
    {
        "tools": "tools",
        "end": END
    }
)
graph.add_edge("tools", "chatbot")

# Compile graph
app = graph.compile()

# Example usage
initial_state = {
    "messages": [
        {
            "role": "user",
            "content": "What is artificial intelligence?"
        }
    ]
}

try:
    response = app.invoke(initial_state)
    print("Final response:", response["messages"][-1].content)
except Exception as e:
    print(f"Error occurred: {str(e)}")
    # Add detailed error information
    import traceback
    print("Full traceback:")
    print(traceback.format_exc())