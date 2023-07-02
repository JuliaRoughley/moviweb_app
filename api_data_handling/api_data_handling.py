import requests

API_address = "http://www.omdbapi.com/?apikey=3ea2912d&"


def get_movie_details_by_name(movie_name):
    """To receive a user input for a movie name, and contact an API using this input
    to search for the movie, and return the required movie details i.e. title, rating, year
    of release and poster url. Returns dict: {"Year": year, "Rating": rating, "Poster": poster} """
    movie_to_add = requests.get(API_address, params={'t': f'{movie_name}', 'r': 'json'}).json()
    if movie_to_add["Response"] == "False":
        return None
    else:
        director = movie_to_add["Director"]
        year = movie_to_add["Year"]
        rating = parses_rating(movie_to_add)
        return {"director": director, "year": year, "rating": rating}


def parses_rating(movie_info):
    """Takes rating as input, this function converts the rating data, and parses
    it into the 'float' type to be useful in functions."""
    if "Ratings" in movie_info and len(movie_info["Ratings"]) > 0:
        rating = movie_info["Ratings"][0]["Value"]
    else:
        rating = "N/A"
    return rating

