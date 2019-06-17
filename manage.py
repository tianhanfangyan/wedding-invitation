from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import MigrateCommand, Migrate

import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

# 集成数据库迁移命令，步骤1执行一次即可，需要修改数据模型后需要迁移执行2、3步骤即可
# 1.创建迁移仓库：python manage.py db init
# 2.创建迁移脚本：python manage.py db migrate --message "initial migration"
# 3.更新数据库：python manage.py db upgrade
manager.add_command("db", MigrateCommand)

# 注册app启动manager
server = Server(host="0.0.0.0", port=9004)
manager.add_command("runserver", server)

# 注册测试manager
@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
