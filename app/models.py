from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class OnlineUser(db.Model):
    __tablename__ = 'onliners'  # __tablename__是用来指明表名的
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('alluser.id'), unique=True)
    ipadd = db.Column(db.String(20))
    # order = db.relationship('Order', uselist=False, backref='odriver')  ########!!!!!!!!!!!!!

    def __repr__(self):
        return '<Driver %r>' % self.id


class User(UserMixin, db.Model):
    __tablename__ = 'alluser'
    id = db.Column(db.Integer, primary_key=True)
    #  个人信息
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)  # 用户名
    password_hash = db.Column(db.String(128), nullable=False)  # 密码
    tel = db.Column(db.String(20), nullable=False)  # 电话
    # 车主信息
    IDcard = db.Column(db.String(64))  # 身份证号
    pic = db.Column(db.String(128), default=None)  # 添加头像
    license_num = db.Column(db.String(64))  # 驾驶证号
    license_type = db.Column(db.String(64))  # 驾驶证类型
    scord = db.Column(db.Integer)
    # 车辆信息
    type = db.Column(db.String(64))  # 车辆类型
    number = db.Column(db.String(64))  # 车牌号
    # 位置信息
    curlat = db.Column(db.Float)
    curlng = db.Column(db.Float)
    onliner = db.relationship('OnlineUser', uselist=False, backref='user')
    confirm = db.Column(db.Boolean)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
