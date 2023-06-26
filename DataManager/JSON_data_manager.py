import json

from DataManager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """Loads the JSON data file, initialises an empty list of users, loops through the data from the json file and
        adds each user as a dictionary to the list,then returns the list of all users"""

        with open(self.filename, "r") as file:
            user_sdata = json.loads(file.read())

        users = []
        for user in user_sdata:
            users.append({"user": user["name"]})

        return users

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        with open(self.filename, "r") as file:
            users_data = json.loads(file.read())

        for user in users_data:
            if user["id"] == user_id:
                return user["movies"]
