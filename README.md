# LangGraph Agentic Workflow Patterns

Hands-on examples of the core agentic workflow patterns implemented with LangGraph: prompt chaining, routing, parallelization, orchestrator-worker, and tool-calling agents.

## What it covers
| File | Pattern |
|---|---|
| `lession_1.py` | Minimal LangGraph chatbot (StateGraph, START/END, `add_messages`) with OpenAI `gpt-4o-mini` |
| `lession_2.py`, `lession2_.py` | Tool-using chatbot with Wikipedia and Arxiv tools, `ToolNode` and `tools_condition` |
| `promt_chaining.py` | Prompt chaining: generate joke -> conditional punchline check -> improve -> polish |
| `routeing.py` | Routing: an LLM with structured output (Pydantic) picks joke / poem / story node |
| `parraltion.py` | Parallelization: joke, story and poem nodes run in parallel and an aggregator merges them |
| `Orchestrator1.py` | Orchestrator-worker: planner produces report sections, workers are fanned out with `Send`, results synthesized (report text uses `data.md` as sample topic material) |
| `tools_.py` | Structured output and `bind_tools` examples |
| `llm_set.py` | Shared `ChatGoogleGenerativeAI` (`gemini-2.0-flash`) instance used by the pattern scripts |
| `demo.ipynb`, `demo.py` | Scratch notebook / script (`demo.py` is an incomplete snippet) |

## Tech stack
Python, LangGraph, LangChain (core, community, OpenAI, Google GenAI), Pydantic, python-dotenv.

## Setup
No requirements file is provided. Install: `langgraph langchain-core langchain-community langchain-openai langchain-google-genai pydantic python-dotenv arxiv wikipedia ipython`.
Create `.env` (gitignored) with `OPENAI_API_KEY` and `GOOGLE_API_KEY`. Scripts are written notebook-style (they display graph images with IPython), so run them in Jupyter/VS Code interactive mode.

## Limitations
Learning notes, not a library: scripts are largely self-contained cells, there are typos in names (`lession`, `routeing`), a bug in `tools_.py` (`multipy` returns a+b), and `demo.py` does not parse.
