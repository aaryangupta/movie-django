import requests
from django.conf import settings



def get_movie_details(imdb_id):
    """
    IMDb ID के आधार पर movie details प्राप्त करें।
    """
    url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&i={imdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}


def search_movies(query, count=25):
    """
    OMDb API से दिए गए query के आधार पर movies fetch करता है।
    count parameter से सुनिश्चित किया जाता है कि कम से कम count movies return हों।
    """
    movies = []
    page = 1
    while len(movies) < count:
        url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&s={query}&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            page_movies = data.get("Search", [])
            if not page_movies:  # अगर कोई movie न मिले तो loop break करें
                break
            movies.extend(page_movies)
        else:
            break
        page += 1
    return movies[:count]