import json
from DataManager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def open_movie_JSON_data(self):
        """Loads the JSON data file and returns it."""
        with open(self.filename, "r") as file:
            user_data = json.load(file)
        return user_data

    def user_exists(self, user_id):
        """Loads the JSON data file and returns true if the user_id locates a matching record"""
        user_data = self.open_movie_JSON_data()
        for user in user_data:
            if user["id"] == user_id:
                return True

        return False

    def get_all_users(self):
        """Loads the JSON data file and returns a list of dictionaries containing user IDs and names"""
        user_data = self.open_movie_JSON_data()

        users = []
        for user in user_data:
            users.append({"id": user["id"], "name": user["name"]})

        return users

    def get_user_movies(self, user_id):
        """Loades the JSON movie data, loops through the data checking the 'id' in the dictionary against the argument 'user_id', if found it returns the list of the users movies, if not it returns nothing"""
        users_data = self.open_movie_JSON_data()
        userid = False

        for user in users_data:
            if user["id"] == user_id:
                return user["movies"]

        if not userid:
            return None

    def add_new_user(self, username):
        """Loads the movie data, creates a new user id for the new user to be added, creates new user"""
        users_data = self.open_movie_JSON_data()
        new_user_id = len(users_data) + 1
        new_user = {
            "id": new_user_id,
            "name": username,
            "movies": []
        }
        users_data.append(new_user)

        with open(self.filename, "w") as file:
            json.dump(users_data, file, indent=4)

    def add_new_movie(self, user_id, title, director, year, rating):
        """Loads data, finds the user that corresponds with the user_id (ifcan't find user
        returns None), access the users movie list in the dictionary and check if the movie
        the user wants to add already exists in the list - if it does it lets the user know, 
        if not the movie is added with a newly generated movie id"""
        with open(self.filename, "r") as file:
            users_data = json.load(file)

        user = next(
            (user for user in users_data if user["id"] == user_id), None)
        if user is None:
            return

        movies = user["movies"]
        if any(movie["name"] == title for movie in movies):
            print(
                f"The movie '{title}' already exists in your list of favorite movies.")
            return

        new_movie_id = len(movies) + 1

        new_movie = {
            "id": new_movie_id,
            "name": title,
            "director": director,
            "year": year,
            "rating": rating
        }
        movies.append(new_movie)

        with open(self.filename, "w") as file:
            json.dump(users_data, file, indent=4)

    def update_movie(self, user_id, movie_id, title, director, year, rating):
        """loads JSON file data, finds the correct user we wish to update the movie for, then finds
        the list of movies and searches for the movie_id - if not foundreturns nothing, if found then updates
        the movie details and saves to the json file."""
        with open(self.filename, "r") as file:
            users_data = json.load(file)

        user = next(
            (user for user in users_data if user["id"] == user_id), None)
        if user is None:
            return

        movie = next(
            (movie for movie in user["movies"] if movie["id"] == movie_id), None)
        if movie is None:
            return

        movie["name"] = title
        movie["director"] = director
        movie["year"] = year
        movie["rating"] = rating

        with open(self.filename, "w") as file:
            json.dump(users_data, file, indent=4)

    def movie_exists(self, user_id, movie_title):
        """Function to find if movie already exists in the database, to be used alongside other functions like 
        add, delete and update movie. Loads the json data, finds user, finds movie"""
        users_data = self.open_movie_JSON_data()
        user = next(
            (user for user in users_data if user["id"] == user_id), None)
        if user:
            movies = user.get("movies", [])
            return any(movie.get("name") == movie_title for movie in movies)
        return False

    def delete_movie(self, user_id, movie_id):
        """loads json data, finds the right user, if not found returns None. Accesses the users movie list,
        Loops through the list looking for matching movie_id, and deletes the movie, then updates the json data
        with new list."""
        users_data = self.open_movie_JSON_data()
        user = next(
            (user for user in users_data if user["id"] == user_id), None)
        if user is None:
            return
        movies = user["movies"]
        for movie in movies:
            if movie["id"] == movie_id:
                movie_to_delete = movie

        movies.remove(movie_to_delete)

        with open(self.filename, "w") as file:
            json.dump(users_data, file, indent=4)

    def get_list_user_ids(self):
        """Gets list of user ids"""
        user_info = self.open_movie_JSON_data()
        user_ids = []
        for user in user_info:
            user_ids.append(user["id"])

        return user_ids
