import os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager





if sys.platform.startswith('win'): # 如果是Windows系统
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= prefix + os.path.join(os.path.dirname(app.root_path), 'data.db') #配置数据库地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭数据库修改的监控
db = SQLAlchemy(app) # 将应用实例传入数据库管理类
app.config['SECRET_KEY'] = 'dev'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典, 等同于{'user':user}


from watchlist import views, errors, commands
