from flask import Flask, render_template, request, redirect
from DataManager.JSON_data_manager import JSONDataManager
from api_data_handling.api_data_handling import get_movie_details_by_name
from urllib.parse import unquote, quote
import logging

data_manager = JSONDataManager("movie_data/movies.json")
app = Flask(__name__)


@app.route('/')
def home():
    """Presents a (simple) welcome page"""
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    """Gets the list of the users of the app and renders the appropriate html template to 
    display a webpage to the user"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def list_users_movies(user_id):
    """Takes user_id as an argument and gets the list of movies for that particular user, then returns it and 
    renders the html template to display the movies to the user. If a user id is entered that doesn't exist, a 
    separate html template is rendered informing the user of the error."""
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
    """Hanles GET and POST requests. Get renders the form html template to fill out a new user
    details, and the form once submitted submits the POST request to add the the new user_details
    to the saved data (in this case a JSON file). Form validation is also used to ensure no blank fields"""
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
    """GET request to render the form html for adding a new movie, the form only needs the name of the movie
    submitting the form creates a POST request - the rest of the movie details are accessed API request, and if
    present are added to the movie list for the specific user. The movie is also checked for to see if it already 
    exists in the user's list, if it does, it informs the user without adding a duplicate movie""" 
    if request.method == 'POST':
        movie = request.form.get('movie')
        if not movie:
            error_message = "Movie name is required."
            return render_template('add_movie.html', error=error_message, user_id=user_id)

        movie_details = get_movie_details_by_name(movie)
        if movie_details is None:
            return render_template('api_false_return.html', user_id=user_id)

        title = movie
        director = movie_details["director"]
        year = movie_details["year"]
        rating = movie_details["rating"]

        if data_manager.movie_exists(user_id, title):
            error_message = f"{title} is already in your list of favorite movies."
            return render_template('add_movie.html', error_message=error_message, user_id=user_id)

        data_manager.add_new_movie(user_id, title, director, year, rating)
        return redirect(f'/users/{user_id}')

    return render_template("add_movie.html", user_id=user_id)


@app.route('/users/<int:user_id>/edit_movie/<int:movie_id>', methods=['GET'])
def edit_movie(user_id, movie_id):
    """To update the movie - can allow form fields to be changed or no change. Looks for movie in the users list,
    but if not found it renders a different html template. The update button next to the movies opens up a prepopulated
    form."""
    user_movies = data_manager.get_user_movies(user_id)
    movie = next((movie for movie in user_movies if movie["id"] == movie_id), None)

    print(movie)

    if movie:
        return render_template('edit_movie.html', user_id=user_id, movie=movie)
    else:
        return render_template('movie_not_found.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['POST'])
def update_movie(user_id, movie_id):
    """The edit_movie GET request opens up this form, and this submits a POST request with any updates 
    the user might have made"""
    title = request.form.get('name')
    director = request.form.get('director')
    year = request.form.get('year')
    rating = request.form.get('rating')

    data_manager.update_movie(user_id, movie_id, title, director, year, rating)
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Each movie has associated with it in html a delete button, which sends POST request with the user and movie
    ids, and activates the delete movie function, removing it from the list"""
    user_id = int(request.form.get('user_id'))
    movie_id = int(request.form.get('movie_id'))
    data_manager.delete_movie(user_id, movie_id)

    return redirect(f'/users/{user_id}')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
