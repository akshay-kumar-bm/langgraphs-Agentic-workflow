from pydantic import BaseModel , Field
from llm_set import llm
class SerachQuery(BaseModel):
    search_query:str=Field(None,description="Query that is optimized web serach ")
    justification :str=Field(None , description="Why this query is relevanr to ther user requied")

structured_llm=llm.with_structured_output(SerachQuery)

ouput=structured_llm.invoke("How does Calcium CT score relate to high Cholestral ?")

def multipy(a :int , b:int)->int :
    return a+b

llm_with_tool=llm.bind_tools([multipy])

result=llm_with_tool.invoke(' what is 3 time of 3')

result.tool_calls


