#  db是数据库对象,login_manager用于管理用户登录
from app import db, login_manager

#  UserMixin提供了一些用户类需要的方法
from flask_login import UserMixin

#  generate_password_hash和check_password_hash用于处理密码加密
from werkzeug.security import generate_password_hash, check_password_hash

#  用户类,代表了数据库中的用户表
class User(UserMixin, db.Model):

    #  db.Integer: 指定列类型为整数  primary_key=True: 将此列设为主键
    id = db.Column(db.Integer, primary_key=True)

    #  db.String(64): 指定列类型为字符串,最大长度64    unique=True: 确保此列的值是唯一的    nullable=False: 不允许此列的值为空
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    password_hash = db.Column(db.String(128))    #  password_hash存储加密后的密码

    # files建立了与File类的关联,表示一个用户可以有多个文件
    files = db.relationship('File', backref='owner', lazy='dynamic')

    #  设置用户密码,不直接存储密码,而是存储密码的加密版本
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #  用于验证用户输入的密码是否正确
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#  文件类,代表数据库中的文件表
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    path = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    #  根据用户ID加载用户对象
    return User.query.get(int(user_id))


#  db.Column() 是 SQLAlchemy 中用于定义数据库表列的方法,帮助我们定义数据库表的结构,指定每一列的数据类型和约束。
#  @login_manager.user_loader    用于告诉 Flask-Login 如何根据用户 ID 加载用户对象
#  User.query.get() 执行从数据库检索用户的操作
