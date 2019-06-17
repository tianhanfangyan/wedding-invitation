FROM python:3.7-alpine3.7

ENV FLASK_CONFIG=production

RUN apk update && apk add --no-cache tzdata

WORKDIR /wedding_invitation

ADD . .

RUN pip install -r ./requirements.txt

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 创建迁移仓库
RUN python manage.py db init

# 创建迁移脚本
RUN python manage.py db migrate --message "initial migration"

# 更新数据库
RUN python manage.py db upgrade

# add a auth user
RUN python db_user.py

# expose default port 9004
EXPOSE 9004

# command
CMD ["python", "manage.py", "runserver"]

