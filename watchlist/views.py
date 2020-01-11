from flask import render_template, url_for, redirect, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from watchlist import db, app
from watchlist.models import User, Movie

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('index')
        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title)>60:
            flash('Invalid input!')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created!')
        return redirect(url_for('index'))
    user = User.query.first()
    movies= Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


# @login_manager.user_loader
# def load_user(user_id):
#     user = User.query.get(int(user_id))
#     return user


@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie= Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year') 
        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid input')        
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Invalid input!')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success!')
            return redirect(url_for('index'))

        flash('Invalid username and password!')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodby!')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form.get('name')

        if not name or len(name) > 20:
            flash('Invalid input!')
            return redirect(url_for('settings'))
        # user = User.query.first()
        # user.name = name
        current_user.name = name # 同上两行的用法
        db.session.commit()
        flash('Settings updated!')
        return redirect(url_for('index'))

    return render_template('settings.html')




if __name__ == '__main__':
    app.run()