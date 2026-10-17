

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from tmdb import client as tmdb_client

@tool
def search_movies(query:str, limit:int=5, config:RunnableConfig= {}):
    """ search the most recent LIMIT Movies from the movie database with maximum of 25
    arguments:
    query:stirng or lookup search across title or content of document
    limit: number of results
    """
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    print('searching with user',user_id)
    response = tmdb_client.search_movie(query, raw = False )
    # if not response.status_code in range(200, 299):
    #     return[]
    try:
        total_results = int(response.get("total_results"))
    except:
        total_results = 0
        
    if total_results == 0:
        return []
        
    if total_results > 25:
        limit =25
    results = response.get("results")[:limit]
    return results


@tool
def movie_detail(movie_id: int, limit:int=5, config:RunnableConfig= {}):
    """ movie detail form the movie database if it exists.
    arguments:
    movie_id: integer form movie search
    """
    configurable = config.get('configurable') or {}
    user_id = configurable.get('user_id')
    print('searching with user', user_id)
    response = tmdb_client.movie_detail(movie_id, raw =False)
    
    return response

movie_discovery_tools=[
    
    search_movies,
    movie_detail
]