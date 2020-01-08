from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os, sys
import click

if sys.platform.startswith('win'): # 如果是Windows系统
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= prefix + os.path.join(app.root_path, 'data.db') #配置数据库地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭数据库修改的监控
db = SQLAlchemy(app) # 将应用实例传入数据库管理类


@app.cli.command() #注册为命令
@click.option('--drop', is_flag=True, help='Create after drop') #设置选项
def initdb(drop):
    '''Initialize the database'''
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.route('/')
def index():
    user = User.query.first()
    movies= Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.cli.command()
def forge():
    '''Generate fake data'''
    db.create_all()
    name = 'Daniel Yuan'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1998'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
]

    user=User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done')



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))




if __name__ == '__main__':
    app.run()