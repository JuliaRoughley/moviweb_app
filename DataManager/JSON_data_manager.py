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

    def get_all_users(self):
        """Loads the JSON data file and returns a list of dictionaries containing user IDs and names"""
        user_data = self.open_movie_JSON_data()

        users = []
        for user in user_data:
            users.append({"id": user["id"], "name": user["name"]})

        return users

    def get_user_movies(self, user_id):
        users_data = self.open_movie_JSON_data()

        for user in users_data:
            if user["id"] == user_id:
                return user["movies"]

        return []  # Return an empty list if user not found

    def add_new_user(self, username):
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
        # Load the JSON data from the file
        with open(self.filename, "r") as file:
            users_data = json.load(file)

        # Find the user for whom you want to add the movie
        user = next((user for user in users_data if user["id"] == user_id), None)
        if user is None:
            # Handle user not found error
            return

        # Access the "movies" list for that user
        movies = user["movies"]

        # Check if the movie already exists in the user's list of movies
        if any(movie["name"] == title for movie in movies):
            # Movie already exists, handle the case appropriately
            print(f"The movie '{title}' already exists in your list of favorite movies.")
            return

        # Generate a new movie ID
        new_movie_id = len(movies) + 1

        # Create the new movie dictionary
        new_movie = {
            "id": new_movie_id,
            "name": title,
            "director": director,
            "year": year,
            "rating": rating
        }

        # Append the new movie dictionary to the "movies" list
        movies.append(new_movie)

        # Save the modified JSON data back to the file
        with open(self.filename, "w") as file:
            json.dump(users_data, file, indent=4)

    def movie_exists(self, user_id, movie_title):
        users_data = self.open_movie_JSON_data()
        user = next((user for user in users_data if user["id"] == user_id), None)
        if user:
            movies = user.get("movies", [])
            return any(movie.get("name") == movie_title for movie in movies)
        return False

    def delete_movie(self, user_id, movie_id):
        users_data = self.open_movie_JSON_data()
        user = next((user for user in users_data if user["id"] == user_id), None)
        if user is None:
            # Handle user not found error
            return
        movies = user["movies"]
        for movie in movies:
            if movie["id"] == movie_id:
                movie_to_delete = movie

        movies.remove(movie_to_delete)

        with open(self.filename, "w") as file:
            json.dump(users_data, file, indent=4)


