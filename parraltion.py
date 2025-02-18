from typing_extensions import TypedDict
from langgraph.graph import StateGraph , START , END
from IPython.display import Image, display
from llm_set import llm

class State(TypedDict):
    topic:str
    joke:str
    story:str
    poem:str
    combined_ouput:str

def call_llm_1(state:State):
    "firsy llm call"
    msg=llm.invoke(f"write a joke about {state['topic']}")
    return {"joke":msg.content}

def call_llm_2(state:State):
    "second llm"
    msg=llm.invoke(f'write a stiry about {state['topic']}')
    return {"story":msg.content}
def call_llm_3(state:State):
    "3rd llm"
    msg=llm.invoke(f"write a poem about {state['topic']}")
    return {'poem':msg.content}

def aggregater(state:State):
    "combination of the 3 llm into a simgle output"
    comibted=f"Here a store , joke and poam about {state['topic']}"
    comibted+=f"\nStore :{state['story']}"
    comibted+=f"\njoke :{state["joke"]}"
    comibted+=f"\npoem :{state["poem"]}"
    return {'combined_ouput':comibted}


workflow=StateGraph(State)
workflow.add_node("jokes",call_llm_1)
workflow.add_node("Story",call_llm_2)
workflow.add_node("poems",call_llm_3)
workflow.add_node("PoemStory&Joke",aggregater)


# workflow.add_edge(START,"jokes")
# workflow.add_edge("jokes","Story")
# workflow.add_edge("Story","poems")
# workflow.add_edge("poems","PoemStory&Joke")
# workflow.add_edge("PoemStory&Joke",END)

workflow.add_edge(START,"jokes")
workflow.add_edge(START,"Story")
workflow.add_edge(START,"poems")
workflow.add_edge("jokes","PoemStory&Joke")
workflow.add_edge("Story","PoemStory&Joke")
workflow.add_edge("poems","PoemStory&Joke")
workflow.add_edge("PoemStory&Joke",END)

chain=workflow.compile()

display(Image(chain.get_graph().draw_mermaid_png()))


result=chain.invoke({"topic":"pen"})
print(result['combined_ouput'])