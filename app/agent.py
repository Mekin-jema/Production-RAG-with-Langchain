# Agent Orchestration with LangGraph
import sys
import os
from pathlib import Path

# Add project root to sys.path to allow running as a direct script
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.append(project_root)

from asyncio import timeout
from typing import Optional
from typing_extensions import TypedDict,Annotated
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langsmith import traceable

from app.config import get_settings
 
 
class AgentState(TypedDict):
    """ State for the production agent.
        Uses Annotated with add_messages reducer for message accumulation.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    error: Optional[str]
    retry_count: int
    model_used: str


class ProductionAgent:
    """
    Production LangGraph agent with:
     - Retry on failure (model fallback)
     - Graceful error handling
     - LangSmith tracing
    """
    def __init__(self):
        settings = get_settings()
        self.llm_primary = ChatOpenAI(
            model=settings.primary_model,
            temperature=0,
            timeout=30,
            max_retries=0,
            api_key=settings.openrouter_api_key
        )
        self.fallback_llm = ChatOpenAI(
            model=settings.fallback_model,
            temperature=0,
            timeout=30,
            max_retries=0,
            api_key=settings.openrouter_api_key 
        )

        self.max_retries = settings.max_retries
        self.graph = self._build_graph()

    def _build_graph(self):
        """ Build the LangGraph State machine."""
        def process_message(state: AgentState) -> dict:
            try:
                response = self.llm_primary.invoke(
                    state['messages']
                )
                return {
                    "messages": [response],
                    "error": None,
                    "model_used": "primary",
                    "retry_count": state.get("retry_count", 0)
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "retry_count": state["retry_count"] + 1,
                    "model_used": ""
                }
        
        def try_fallback(state: AgentState) -> dict:
            """Fallback to secondary model."""
            try:
                response = self.fallback_llm.invoke(state["messages"])
                return {
                    "messages": [response],
                    "error": None,
                    "model_used": "fallback",
                }
            except Exception as e:
                return {
                    "error": str(e),
                    "retry_count": state["retry_count"] + 1,
                    "model_used": ""
                }

        def handle_error(state: AgentState) -> dict:
            """Log and return final error state."""
            return {
                "messages": [AIMessage(content="I'm sorry, I'm having trouble processing your request right now. Please try again later.")],
                "model_used": "error_handler"
            }

        def route_after_process(state: AgentState) -> str:
            """Decide what to do after primary model attempt."""
            if state.get("error") is None:
                return "done"
            elif state["retry_count"] < self.max_retries:
                return "fallback"
            else:
                return "error"

        def route_after_fallback(state: AgentState) -> str:
            """Decide what to do after fallback model attempt."""
            if state.get("error") is None:
                return "done"
            elif state["retry_count"] < self.max_retries:
                return "retry"
            else:
                return "error"

        # Build the graph
        graph = StateGraph(AgentState)
        graph.add_node("process_message", process_message)
        graph.add_node("try_fallback", try_fallback)
        graph.add_node("handle_error", handle_error)

        # add edges
        graph.add_edge(START, "process_message")
        graph.add_edge("handle_error", END)

        graph.add_conditional_edges(
            "process_message",
            route_after_process,
            {"done": END, "fallback": "try_fallback", "error": "handle_error"}, 
        )
        graph.add_conditional_edges(
            "try_fallback",
            route_after_fallback,
            {"done": END, "retry": "process_message", "error": "handle_error"},
        )

        # Compile the graph
        return graph.compile()
        
    @traceable
    def invoke(self, message: str) -> dict:
        """Invoke the production agent with a user message.
        Returns:
            {"response": str, "model_used": str, "error": str|None}
        """
        result = self.graph.invoke({
            "messages": [HumanMessage(content=message)],
            "error": None,
            "retry_count": 0,
            "model_used": ""
        })
        return {
            "response": result["messages"][-1].content,
            "model_used": result.get("model_used"),
            "error": result.get("error")    
        }


def demo_agent():
    print("=== Production Agent Demo ===")
    try:
        agent = ProductionAgent()
        print("Invoking agent with query: 'Explain Python in 1 sentence.'")
        result = agent.invoke("Explain Python in 1 sentence.")
        print(f"Response: {result['response']}")
        print(f"Model Used: {result['model_used']}")
        print(f"Error: {result['error']}")
    except Exception as e:
        print(f"Failed to run agent: {e}")


if __name__ == "__main__":
    demo_agent()


            
            


    
    
