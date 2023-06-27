from flask import Flask, render_template, request, redirect
from DataManager.JSON_data_manager import JSONDataManager
import json

app = Flask(__name__)
data_manager = JSONDataManager("movie_data/movies.json")


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def list_users_movies(user_id):
    users_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', users_movies=users_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_new_user():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            error_message = "Username is required."
            return render_template('add_user.html', error=error_message)

        data = data_manager.open_movie_JSON_data()

        for user in data:
            if user["name"] == username:
                error_message = "Username already exists. Please choose a different username."
                return render_template('add_user.html', error=error_message)

        data_manager.add_new_user(username)
        return redirect('/users')

    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie')
def add_new_movie():
    pass


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie():
    pass


@app.route('/users/<user_id>/edit_movie/<movie_id>')
def edit_movie():
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    pass


if __name__ == '__main__':
    app.run(debug=True)
