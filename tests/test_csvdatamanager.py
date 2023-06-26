from DataManager.CSV_data_manager import CSVDataManager


def test_csvdatamanager_getallusers():
    test_class = CSVDataManager("test_csvdatamanager.csv")
    data = test_class.get_all_users()
    print(data)
    assert data is not None
    assert len(data) == 2
    assert data[0]["user"] == "Alice"
    assert data[1]["user"] == "Bob"


def test_csvdatamananger_getusermovies():
    test_class = CSVDataManager("test_csvdatamanager.csv")
    movies = test_class.get_user_movies(1)
    print(movies)

