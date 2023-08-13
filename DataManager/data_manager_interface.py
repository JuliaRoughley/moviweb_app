from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """To get a list of all the users who have an account in the moviweb app"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """To get and return a list of the favourite movies for the specidied uesr_id"""
        pass

    @abstractmethod
    def add_new_user(self):
        """To add a new user account to the moviweb app"""
        pass

    @abstractmethod
    def add_new_movie(self):
        """To add a new movie to a users list of favourite movies in the moviweb app"""
        pass