import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    CSRF_ENABLED = True
    # 密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you own secret key'

    template_path = os.path.join(os.path.dirname(__file__), "templates")
    static_path = os.path.join(os.path.dirname(__file__), "static")

    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_RECORD_QUERIES = True
    # slow database query threshold (in seconds)
    DATABASE_QUERY_TIMEOUT = 0.5


# 开发环境的配置
class DevelopmentConfig(Config):
    DEBUG = True
    # 数据库URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'wedding.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 测试环境的配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'wedding_dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 生产环境的配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'weeding_pro.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
