import csv
from DataManager.data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """Loads the CSV data file, initialises an empty list of users, loops through the data from the CSV file and
               adds each user as a dictionary to the list,then returns the list of all users"""
        users = []

        with open(self.filename, "r") as file:
            users_data = csv.DictReader(file)
            for row in users_data:
                user_name = row["name"]
                is_duplicate = False
                for user in users:
                    if user["user"] == user_name:
                        is_duplicate = True
                        break

                if not is_duplicate:
                    user = {
                        "user": user_name
                    }
                    users.append(user)

        return users

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        movies = []

        with open(self.filename, "r") as file:
            users_data = list(csv.DictReader(file))

        for row in users_data:
            if int(row["id"]) == user_id:
                for key, value in row.items():
                    if key.startswith("movie"):
                        movie_id = value.strip()
                        if movie_id:
                            movie = {
                                "id": int(row["id"]),
                                "name": row["movie_name"],
                                "director": row["director"],
                                "year": int(row["year"]),
                                "rating": float(row["rating"])
                            }
                            movies.append(movie)

        return movies if movies else []  # Return an empty list if no movies exist for the user

    def add_new_user(self):
        pass

    def add_new_movie(self):
        pass
