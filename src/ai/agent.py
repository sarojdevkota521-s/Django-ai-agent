# from langgraph.prebuilt import create_react_agent
# from ai.tools import document_tools
# from ai.llms import get_openai_model


# def get_document_agent(model=None, checkpointer =None):
#     model = get_openai_model()
#     agent= create_react_agent(
#         model=model,
#         tools=document_tools,
#         prompt="you are a helpful assistant in managing a user's documents within this app" , 
#         checkpointer = checkpointer    
#     )
    
#     return agent

from langgraph.prebuilt import create_react_agent, ToolNode
from ai.tools import document_tools, movie_discovery_tools
from ai.llms import get_openai_model


def get_document_agent(model=None, checkpointer=None):
    model = model or get_openai_model()
    tool_node = ToolNode(document_tools, handle_tool_errors=True)
    return create_react_agent(
        model=model,
        tools=tool_node,
        prompt="You are a helpful assistant in managing a user's documents within this app",
        checkpointer=checkpointer,
        name="Document-Assistant-Agent"
    )
    
    
def get_movie_discovery_agent(model=None, checkpointer=None):
    model = model or get_openai_model()
    tool_node = ToolNode(movie_discovery_tools, handle_tool_errors=True)
    return create_react_agent(
        model=model,
        tools=tool_node,
        prompt="You are a helpful assistant in finding and discovering informaiton about moviews. ",
        checkpointer=checkpointer,
        name = "Movie-Discovery-Assistant-Agent"
    )