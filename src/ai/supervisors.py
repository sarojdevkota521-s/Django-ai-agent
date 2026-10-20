from langgraph_supervisor import create_supervisor

from ai.llms import get_openai_model
from ai import agent


def get_supervisor(model = None, checkpointer=None ):
    llm_model = get_openai_model(model=model)
    return create_supervisor(
        agents = [
            agent.get_document_agent(), 
            agent.get_movie_discovery_agent(),
            
        ],
        model = llm_model,
        prompt=( " You manage a document management assistant and a"
                "movie discovery assistant. assign work to them.")
        
    ).compile(checkpointer =checkpointer)