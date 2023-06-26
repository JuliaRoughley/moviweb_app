from DataManager.JSON_data_manager import JSONDataManager


def test_jsondatamanager_getallusers():
    test_class = JSONDataManager("test_jsondatamanager.json")
    data = test_class.get_all_users()
    assert data is not None
    assert len(data) == 2
    assert data[0]["user"] == "Alice"
    assert data[1]["user"] == "Bob"


def test_jsondatamananger_getusermovies():
    test_class = JSONDataManager("test_jsondatamanager.json")
    movies = test_class.get_user_movies(1)
    print(movies)

