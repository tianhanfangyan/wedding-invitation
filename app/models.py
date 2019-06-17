from app import db
from flask import current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    he = db.Column(db.String(64)) # 新郎姓名
    she = db.Column(db.String(64)) # 新娘姓名
    date = db.Column(db.String(64)) # 婚礼日期
    lunar = db.Column(db.String(64)) # 农历日期
    hotel = db.Column(db.String(128)) # 酒店名称
    address = db.Column(db.String(128)) # 酒店地址
    lat = db.Column(db.Integer) # 经度
    lng = db.Column(db.Integer) # 纬度
    msg = db.Column(db.String) # 分享文字
    images = db.relationship('Images', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User_Info %r>' % (self.address)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(128), index=True, unique=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Images %r>' % (self.src)

class Comments(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    msg = db.Column(db.String(128), index=True)         # 祝福文字
    nickname = db.Column(db.String(128), index=True)    # 微信别名
    face = db.Column(db.String(128), index=True)        # 微信头像

    def __repr__(self):
        return '<id %r>' % (self.id)

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)         # http_auth用户名
    password_hash = db.Column(db.String(128), index=True)   # http_auth密码

    def __repr__(self):
        return '<username %r>' % (self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):

        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        auth = Auth.query.get(data['id'])
        return auth