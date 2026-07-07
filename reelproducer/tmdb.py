import os
import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY")



def search_movie(movie_name):
    url = "https://api.themoviedb.org/3/search/movie"

    response = requests.get(
        url,
        params={
            "api_key": TMDB_API_KEY,
            "query": movie_name
        }
    )
    print(response.status_code)
    print(response.text)
    
    data = response.json()

    if not data["results"]:
        return None

    return data["results"][0]


def download_poster(movie):

    if not movie["poster_path"]:
        return

    os.makedirs("assets", exist_ok=True)

    poster_url = (
        f"https://image.tmdb.org/t/p/original{movie['poster_path']}"
    )

    image = requests.get(poster_url)
    rank = movie.get("rank", "")

    filename = f"{rank}_{movie['title']}".replace("/", "-")

    with open(f"assets/{filename}.jpg", "wb") as f:
        f.write(image.content)

    print("Downloaded:", filename)