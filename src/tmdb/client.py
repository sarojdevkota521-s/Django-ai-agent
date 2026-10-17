import requests
from django.conf import settings
url = "https://api.themoviedb.org/3/search/movie?query=mission%20impossible&include_adult=false&language=en-US&page=1"


#google sheets-> oauth2

def get_headers():
    return {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_API_KEY}"
}

def search_movie(query:str, page:int = 1, raw=False):
    url="https://api.themoviedb.org/3/search/movie"
    params={
        "query":query,
        "page": page,
        "include_adult":False,
        "language":"en-US",
        
    }
    headers=get_headers()
    response =requests.get(url, headers = headers, params= params )
    if raw:
        return response
    return response.json()

def movie_detail(movie_id:int, raw=False):
    url="https://api.themoviedb.org/3/movie/{movie_id}"
    params={
        
        "include_adult":False,
        "language":"en-US",
        
    }
    headers=get_headers()
    response =requests.get(url, headers = headers, params= params )
    if raw:
        return response
    return response.json()