from flask import Flask, render_template, request, redirect
from DataManager.JSON_data_manager import JSONDataManager
from api_data_handling.api_data_handling import get_movie_details_by_name
from urllib.parse import unquote, quote
import logging

data_manager = JSONDataManager("movie_data/movies.json")
#logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.INFO,
#                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def list_users_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    if user_movies is None or len(user_movies) == 0:
        if not data_manager.user_exists(user_id):
            return render_template('no_such_user.html')
   
    success_message = request.args.get("success_message")
    if success_message:
        success_message = unquote(success_message)

    return render_template('user_movies.html', users_movies=user_movies, user_id=user_id, success_message=success_message)


@app.route('/add_user', methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            blank_field_error = "Username is required."
            return render_template('add_user.html', blank_field_error=blank_field_error)

        data = data_manager.open_movie_JSON_data()

        for user in data:
            if user["name"] == username:
                error_message = "Username already exists. Please choose a different username."
                return render_template('add_user.html', error=error_message)

        data_manager.add_new_user(username)
        return redirect('/users')

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=["GET", "POST"])
def add_new_movie(user_id):
    if request.method == 'POST':
        movie = request.form.get('movie')
        if not movie:
            error_message = "Movie name is required."
            return render_template('add_movie.html', error=error_message)

        movie_details = get_movie_details_by_name(movie)
        if movie_details is None:
            error_message = f"I'm sorry, {movie} doesn't exist in the database."
            return render_template('add_movie.html', error=error_message)

        title = movie
        director = movie_details["director"]
        year = movie_details["year"]
        rating = movie_details["rating"]

        if data_manager.movie_exists(user_id, title):
            error_message = f"{title} is already in your list of favorite movies."
            return render_template('add_movie.html', error=error_message)

        data_manager.add_new_movie(user_id, title, director, year, rating)
        return redirect(f'/users/{user_id}')

    return render_template("add_movie.html", user_id=user_id)


@app.route('/users/<int:user_id>/edit_movie/<int:movie_id>', methods=['GET'])
def edit_movie(user_id, movie_id):
    user_movies = data_manager.get_user_movies(user_id)
    movie = next((movie for movie in user_movies if movie["id"] == movie_id), None)

    print(movie)

    if movie:
        return render_template('edit_movie.html', user_id=user_id, movie=movie)
    else:
        return "Movie not found"  # Or redirect to an error page


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['POST'])
def update_movie(user_id, movie_id):
    title = request.form.get('name')
    director = request.form.get('director')
    year = request.form.get('year')
    rating = request.form.get('rating')

    data_manager.update_movie(user_id, movie_id, title, director, year, rating)
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie():
    # Get the user_id and movie_id from the form data
    user_id = int(request.form.get('user_id'))
    movie_id = int(request.form.get('movie_id'))

    # Call the delete_movie function from the JSON data manager
    data_manager.delete_movie(user_id, movie_id)

    return redirect(f'/users/{user_id}')
