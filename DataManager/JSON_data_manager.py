import json

from DataManager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """Loads the JSON data file and returns a list of dictionaries containing user IDs and names"""
        with open(self.filename, "r") as file:
            user_data = json.load(file)

        users = []
        for user in user_data:
            users.append({"id": user["id"], "name": user["name"]})

        return users

    def get_user_movies(self, user_id):
        with open(self.filename, "r") as file:
            users_data = json.load(file)

        for user in users_data:
            if user["id"] == user_id:
                return user["movies"]

        return []  # Return an empty list if user not found

