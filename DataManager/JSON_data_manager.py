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

        with open("movie_data/movies.json", "w") as file:
            json.dump(users_data, file, indent=4)


