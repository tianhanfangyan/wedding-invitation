from . import api
from app import db, httpauth, get_logger
from app.models import User, Comments

from flask import request, jsonify
from flask_sqlalchemy import get_debug_queries

logger = get_logger(__name__)

# 每次请求之后
@api.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= 0.5:
            print("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response

# 添加新人信息
@api.route("/api/add/userinfo", methods=["POST"])
@httpauth.login_required
def get_invitation():
    if not request.json:
        return jsonify({"status": 0, "msg": "参数有问题!!!"})
    try:
        he = request.json.get('he')  # 新郎姓名
        she = request.json.get('she')  # 新娘姓名
        date = request.json.get('date') # 婚礼日期
        lunar = request.json.get('lunar')  # 农历日期
        hotel = request.json.get('hotel') # 酒店名称
        address = request.json.get('address')  # 酒店地址
        lat = request.json.get('lat')  # 经度
        lng = request.json.get('lng')  # 纬度
        msg = request.json.get('msg')  # 分享文字

        user = User(he=he, she=she, date=date, lunar=lunar, hotel=hotel, address=address, lat=lat, lng=lng, msg=msg)
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": 0, "msg": "插入新人信息成功!!!"})
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": -1, "msg": "插入新人信息失败!!!"})

# 变量规则，为url增加变量部分，将特定字符标记为<variable_name>，将作为参数传到你的函数中
# 也可指定一个可选的转换器<converter:variable_name>将变量转换为特定的数据类型。
# int，float，path
# 删除新人信息
@api.route("/api/delete/userinfo/<int:id>", methods=["GET"])
@httpauth.login_required
def delete_userinfo(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": 0, "msg": "删除新人信息成功!!!"})
    except Exception as e:
        logger.info(e)
        return jsonify({"status": -1, "msg": "删除新人信息失败!!!"})

# 查询全部新人信息
@api.route("/api/query/userinfo", methods=["GET"])
@httpauth.login_required
def select_userinfo():
    data_list = []
    user_list = User.query.all()
    try:
        for user in user_list:
            data_list.append({"id": user.id, "he": user.he, "she": user.she, "date": user.date})
        return jsonify({"status": 0, "msg": "查询成功!!!", "data": data_list})
    except Exception as e:
        return jsonify({"status": -1, "msg": "查询失败!!!"})

# 修改新人信息
@api.route("/api/update/userinfo", methods=["POST"])
@httpauth.login_required
def update_userinfo():
    if not request.json:
        return jsonify({"status": 0, "msg": "参数有问题!!!"})
    try:
        id = request.json.get('id')
        he = request.json.get('he')  # 新郎姓名
        she = request.json.get('she')  # 新娘姓名
        date = request.json.get('date') # 婚礼日期
        lunar = request.json.get('lunar')  # 农历日期
        hotel = request.json.get('hotel') # 酒店名称
        address = request.json.get('address')  # 酒店地址
        lat = request.json.get('lat')  # 经度
        lng = request.json.get('lng')  # 纬度
        msg = request.json.get('msg')  # 分享文字

        User.query.filter_by(id=id).update({"he":he, "she":she, "date":date, "lunar":lunar, "hotel":hotel,
                                            "address":address, "lat":lat, "lng":lng, "msg":msg})
        db.session.commit()
        return jsonify({"status": 0, "msg": "修改新人信息成功!!!"})
    except Exception as e:
        logger.info(e)
        return jsonify({"status": -1, "msg": "修改新人信息失败!!!"})

# 获取婚纱照信息
@api.route("/api/getmarryimages", methods=["GET"])
@httpauth.login_required
def get_images():
    data_list = []
    try:
        data_list = [{"name": "image1", "path": "static/image/marry/img1.jpg"},
                     {"name": "image2", "path": "static/image/marry/img2.jpg"},
                     {"name": "image3", "path": "static/image/marry/img3.jpg"},
                     {"name": "image3", "path": "static/image/marry/img4.jpg"}
                 ]
        return jsonify({"status": 0, "msg":"获取婚纱照信息成功.", "data": data_list})
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": -1, "msg":"获取婚纱照信息失败.", "data": data_list})

# 获取we信息
@api.route("/api/getmarryinfo", methods=["GET"])
@httpauth.login_required
def get_marry_info():
    try:
        user = User.query.get(1)
        return jsonify({"status": 0, "msg":"获取新人信息成功.", "data":{"he": user.he, "she": user.she, "date": user.date, "lunar": user.lunar, "hotel": user.hotel, "address": user.address}})
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": -1, "msg":"获取新人信息失败.", "data": {}})

# 获取酒店位置信息
@api.route("/api/gethotelinfo", methods=["GET"])
@httpauth.login_required
def get_hotel_info():
    try:
        user = User.query.get(1)
        return jsonify({"status": 0, "msg":"获取酒店位置信息成功.", "data": {"latitude": float(user.lat), "longitude": float(user.lng)}})
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": -1, "msg":"获取酒店位置信息失败.", "data": {}})

# 添加祝福评论
@api.route("/api/submitbless", methods=["POST"])
@httpauth.login_required
def add_commits():
    if not request.json:
        return jsonify({"status": 0, "msg": "添加祝福消息为空."})

    try:
        msg = request.json.get("bless")
        nickname = request.get("nickname")
        face = request.get("face")
        # instert into db
        comments = Comments(msg=msg, nickname=nickname, face=face)
        db.session.add(comments)
        db.session.commit()
        return jsonify({"status": 0, "msg": "添加祝福信息成功."})
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": -1, "msg": "添加祝福信息失败, 请重试."})

# 获取所有祝福评论
@api.route("/api/getallbless", methods=["GET"])
@httpauth.login_required
def get_commits():
    data_list = []
    try:
        all_comments = Comments.query.all()
        for comments in all_comments:
            msg = comments.msg
            nickname = comments.nickname
            face = comments.face
            data_list.append({"nickname":nickname, "face":face, "bless":msg})
        return jsonify({"status": 0, "data": data_list, "msg": "获取所有祝福成功."})
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": -1, "data": data_list, "msg": "获取所有祝福失败, 请重试."})
