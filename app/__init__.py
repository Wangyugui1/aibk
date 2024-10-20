from flask import Flask
from flask_sqlalchemy import SQLAlchemy    # SQLAlchemy: 用于数据库操作
from flask_login import LoginManager    # LoginManager: 用于处理用户登录
from config import Config    # Config: 包含应用配置的类

db = SQLAlchemy()    # 创建SQLAlchemy实例,用于数据库操作
login_manager = LoginManager()     # 创建LoginManager实例,用于管理用户登录

# 一个应用工厂函数,用于创建和配置Flask应用实例
def create_app():
    
    #  创建Flask应用实例
    app = Flask(__name__)

    # 从Config对象加载配置
    app.config.from_object(Config)

    # 初始化数据库与应用的连接
    db.init_app(app)

    # 初始化登录管理器
    login_manager.init_app(app)

    # 设置登录页面的视图函数
    login_manager.login_view = 'auth.login'

    # 导入了两个蓝图(main和auth),并将它们注册到应用中
    from app.routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
