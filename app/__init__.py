import os
import logging
from logging.config import fileConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from conf.config import config

# 日志
fileConfig('conf/log-app.conf')

httpauth = HTTPBasicAuth()
db = SQLAlchemy()

def get_logger(name):
    return logging.getLogger(name)

def create_app(config_name):

    # 创建app
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))
    # 导致指定的配置对象
    app.config.from_object(config[config_name])

    # 扩展模块
    db.init_app(app)

    # 注册auth蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # 注册api蓝图
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # 注册main蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app




