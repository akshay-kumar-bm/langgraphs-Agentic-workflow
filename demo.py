from typing_extensions import TypedDict

# Define the State type with required fields
class State1(TypedDict):
    topic: int
    joke: str
    improved_joke: str
    final_joke: str


state : State1 ={"topic":"t","joke":"hi","final_joke":}
print(state)