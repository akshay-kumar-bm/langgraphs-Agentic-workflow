from typing_extensions import TypedDict
from langgraph.graph import StateGraph , START , END
from IPython.display import Image, display
from llm_set import llm

class State(TypedDict):
    topic:str="cat"
    joke:str
    improved_joke:str
    final_joke:str

def genarate_joke(state:State):
    """first llm call"""
    msg=llm.invoke(f"write a short joke about : {state['topic']}")
    return {"joke":msg.content}

def cheak_punchline(state:State):
    "get the funtion cheak if the joke has punchline "
    if "?" in state['joke'] or "!" in state['joke']:
        return "Fail"
    return "Pass"

def improved_joke(state:State):
    "secod llm call to imporve the joke"
    msg=llm.invoke(f"Make this joke funnier by adding wordplay: {state['joke']}. ouput:JOKE")
    return {"improved_joke":msg.content}

def polish_joke(state:State):
    "third llm call for final polish"
    msg=llm.invoke(f"add a suprising twish to the joke: {state['improved_joke']}. ouput:Short Joke")
    return {"final_joke":msg.content}

workflow=StateGraph(State)
workflow.add_node("genarate_joke",genarate_joke)
workflow.add_node("improve_joke",improved_joke)
workflow.add_node("polish_joke",polish_joke)

workflow.add_edge(START,"genarate_joke")
workflow.add_conditional_edges("genarate_joke",cheak_punchline,{'Fail':"improve_joke","Pass":END})
workflow.add_edge("improve_joke","polish_joke")
workflow.add_edge("polish_joke",END)

chain=workflow.compile()

display(Image(chain.get_graph().draw_mermaid_png()))
state = chain.invoke({'topic':"hi"})
print("Initial joke:")
print(state["joke"])
print("\n--- --- ---\n")
if "improved_joke" in state:
    print("Improved joke:")
    print(state["improved_joke"])
    print("\n--- --- ---\n")

    print("Final joke:")
    print(state["final_joke"])
else:
    print("Joke failed quality gate - no punchline detected!")