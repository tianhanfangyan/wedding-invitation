from . import auth
from app import get_logger, httpauth, db
from app.models import Auth

from flask import g, request, jsonify

logger = get_logger(__name__)

@httpauth.verify_password
def verify_password(username, password):
    # try to authenticate with username/password
    auth = Auth.query.filter_by(username=username).first()
    if not auth or not auth.verify_password(password):
        return False
    g.auth = auth
    return True


@auth.route("/auth/updatepwd", methods=["POST"])
@httpauth.login_required
def updatepwd():
    if not request.json:
        return jsonify({"status": 0, "msg": "参数有问题!!!"})
    try:
        old_username = request.json['username']
        new_password = request.json['password']
        auth_user = Auth.query.filter_by(username=old_username).first()
        if not auth_user:
            return jsonify({"status": -1, "msg": "账号名错误!!!"})
        auth_user.hash_password(new_password)
        Auth.query.filter_by(id=1).update({"password_hash": auth_user.password_hash})
        db.session.commit()

        return jsonify({"status": 0, "msg": "密码修改成功!!!"})
    except Exception as e:
        logger.exception(e)
        return jsonify({"status": -1, "msg": "密码修改失败!!!"})