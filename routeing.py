from typing_extensions import TypedDict,Literal
from langgraph.graph import StateGraph , START , END
from IPython.display import Image, display
from llm_set import llm
from pydantic import BaseModel, Field

class State(TypedDict):
    input:str
    Decision:str
    ouput:str

class Deciside(BaseModel):
    intent:Literal["Joke","poem","story"]=Field(None,description="The next step in the routing process")

Deciside_llm=llm.with_structured_output(Deciside)

def llm_joke(state:State):
    msg=llm.invoke(f"Write a joke for given topic {state['input']}")
    return {"ouput":msg.content}

def llm_poem(state:State):
    msg=llm.invoke(f"write a poem for given topic :{state['input']}")
    return {"output":msg.content}

def llm_store(state:State):
    msg=llm.invoke(f"write a story for a given topic:{state['input']}")
    return {'output':msg.content}

def deside(state:State):
    msg=Deciside_llm.invoke(f"Route the input to story, joke, or poem based on the user's request .Request:{state['input']}")
    return {'Decision':msg.intent}

def route_desisio(state:State):
    if state['Decision']=="Joke":
        return "llm_joke"
    elif state['Decision']=="poem":
        return "llm_poem"
    elif state['Decision']=="story":
        return "llm_store"
    
router_bulder=StateGraph(State)
router_bulder.add_node("llm_joke",llm_joke)
router_bulder.add_node("llm_poem",llm_poem)
router_bulder.add_node("llm_store",llm_store)
router_bulder.add_node("route_desisio",deside)

router_bulder.add_edge(START,"route_desisio")
router_bulder.add_conditional_edges("route_desisio",route_desisio,{
    "llm_joke":"llm_joke",
    "llm_poem":"llm_poem",
    "llm_store":"llm_store",
})
router_bulder.add_edge("llm_joke",END)
router_bulder.add_edge("llm_poem",END)
router_bulder.add_edge("llm_store",END)

router_bulder=router_bulder.compile()

display(Image(router_bulder.get_graph().draw_mermaid_png()))


resut=router_bulder.invoke({"input":"tell me a joke on pen"})
