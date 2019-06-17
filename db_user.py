from app import create_app, models
from flask_sqlalchemy import SQLAlchemy

import optparse
import os


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
db = SQLAlchemy(app)

# 初始化创建一个admin账号，一旦部署后，切记修改其密码。
# username: admin
# password: 123456
parser = optparse.OptionParser()

parser.add_option("--username", action="store", type="string", default="admin", dest="username")
parser.add_option("--password", action="store", type="string", default="123456", dest="password")

opt, args = parser.parse_args()

username = opt.username
password = opt.password

# add a auth user
auth = models.Auth(username=username)
auth.hash_password(password=password)

# commit
db.session.add(auth)
db.session.commit()
print("创建用户账号成功")