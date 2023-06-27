from DataManager.JSON_data_manager import JSONDataManager


def test_jsondatamanager_getallusers():
    test_class = JSONDataManager("test_jsondatamanager.json")
    data = test_class.get_all_users()
    assert data is not None
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2
    print(data)


def test_jsondatamananger_getusermovies():
    test_class = JSONDataManager("test_jsondatamanager.json")
    movies = test_class.get_user_movies(1)
    print(movies)

