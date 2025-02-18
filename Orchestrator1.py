from typing_extensions import TypedDict,Literal,List , Annotated
from langgraph.graph import StateGraph , START , END
from IPython.display import Image, display
from llm_set import llm
from pydantic import BaseModel, Field
from langgraph.constants import Send
import operator

from langchain_core.messages import HumanMessage, SystemMessage

class Section(BaseModel):
    name:str=Field(None, description="Name for this section of the report")
    desciption:str=Field(None, description="Brief overview of the main topics and concepts to be covered in this section.")

class Sections(BaseModel):
    section: List[Section]=Field(description="Sections of the report.")

planer=llm.with_structured_output(Sections)

class State(TypedDict):
    topic:str
    sections:list[Section]
    completed_section:Annotated[list , operator.add]
    final_report:str

class WorkerState(TypedDict):
    section:Section
    completed_section:Annotated[list,operator.add]

def orchestrator(state:State):
    "this generate the plain for the report"
    report_sections=planer.invoke(
        [
            SystemMessage(content="Generate a plan for the report"),
            HumanMessage(content=f"here is the report topic:{state['topic']}")
        ]
    )
    return {"sections":report_sections.section}

def llm_call(state:WorkerState):
    "worker write the a secion of the report"
    section=llm.invoke([
        SystemMessage(content="Write a report section following the provided name & descritopn .Include  no preamble for each section. Use markdown formatting."),
        HumanMessage(content=f"Here is the section name: {state['section'].name} and description: {state['section'].desciption}")
    ])
    return {'completed_section':[section.content]}

def synthesizer(state:State):
    "Synthsixe full report from sections"
    completed_section=state['completed_section']

    completed_report_section="\n\n--\n\n".join(completed_section)

    return {'final_report':completed_report_section}

def assign_workers(state:State):
    "assgin a worker to each section in the plan"
    return [Send("llm_call",{"section":s}) for s in state["sections"]]

orchestrator_worker_bulder=StateGraph(State)

orchestrator_worker_bulder.add_node("orchestrator",orchestrator)
orchestrator_worker_bulder.add_node("llm_call",llm_call)
orchestrator_worker_bulder.add_node("synthesizer",synthesizer)

orchestrator_worker_bulder.add_edge(START,"orchestrator")
orchestrator_worker_bulder.add_conditional_edges("orchestrator",
                                                 assign_workers,["llm_call"])
orchestrator_worker_bulder.add_edge("llm_call","synthesizer")
orchestrator_worker_bulder.add_edge("synthesizer",END)

orchestrator_work=orchestrator_worker_bulder.compile()

display(Image(orchestrator_work.get_graph().draw_mermaid_png()))
state = orchestrator_work.invoke({"topic": "give me name for dog from A to Z"})

from IPython.display import Markdown
Markdown(state["final_report"])

