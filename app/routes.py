import os

#    Blueprint：用于组织路由    render_template：用于渲染HTML模板    redirect和url_for：用于页面重定向
#    flash：用于显示消息        current_app：表示当前运行的Flask应用    request：用于处理HTTP请求
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask_login import login_user, login_required, logout_user, current_user  #  导入处理用户登录的功能

from werkzeug.utils import secure_filename    # 导入安全处理文件名的函数
from app import db
from app.models import User, File
import requests


#  创建了两个Blueprint对象：
#      main：用于主要功能的路由
#      auth：用于认证相关功能的路由
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

def allowed_file(filename):
    #  检查文件名是否合法
    #  filename.rsplit('.', 1)[1].lower()：获取文件扩展名并转为小写
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required  #  表示用户必须登录才能访问这个页面
def dashboard():
    files = current_user.files.all()  # 获取当前登录用户的所有文件
    return render_template('dashboard.html', files=files)

#  文件上传路由
@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:  #  检查请求中是否包含文件
        flash('No file part')
        return redirect(url_for('main.dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.dashboard'))
    if file and allowed_file(file.filename): # 如果文件存在且文件名合法
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        new_file = File(filename=filename, path=file_path, user_id=current_user.id)  # 创建新的File对象并保存到数据库
        db.session.add(new_file) # session 是数据库会话,它代表了与数据库的交互
        db.session.commit()
        flash('File uploaded successfully')
    return redirect(url_for('main.dashboard'))

@main.route('/delete/<int:file_id>')  #  <int:file_id>是URL参数
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)  #  获取文件对象,如果不存在则返回404错误
    if file.user_id != current_user.id:  # 检查当前用户是否有权删除此文件
        flash('You are not authorized to delete this file')
        return redirect(url_for('main.dashboard'))
    os.remove(file.path)
    db.session.delete(file)
    db.session.commit()
    flash('File deleted successfully')
    return redirect(url_for('main.dashboard'))

@main.route('/query', methods=['POST']) # AI查询路由，只接受POST请求
@login_required
def query_ai():
    query = request.form.get('query')
    files = current_user.files.all()
    file_contents = []
    for file in files:
        with open(file.path, 'r') as f:
            file_contents.append(f.read()) # 打开每个文件并读取其内容,将内容添加到 file_contents 列表中
    
    context = "\n".join(file_contents)    # 将所有文件内容合并成一个字符串,用换行符分隔
    
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {current_app.config['DEEPSEEK_API_KEY']}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are an AI assistant specialized in analyzing and answering questions based on user-provided documents. Your task is to carefully review the given context and provide accurate, relevant answers to the user's questions."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ]
        }
    )
    
    if response.status_code == 200:
        ai_response = response.json()['choices'][0]['message']['content']
    else:
        ai_response = "Sorry, I couldn't process your request at this time."
    
    return ai_response

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':    # 检查请求方法是否为POST,即用户是否提交了注册表单
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        #  查询数据库,检查用户名是否已存在
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        #  查询数据库,检查邮箱是否已存在
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # User.query 创建一个查询对象     filter_by(username=username) 筛选出用户名匹配的记录    first() 返回查询的第一个结果,如果没有匹配则返回None
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            #    如果用户存在且密码正确,使用 Flask-Login 的 login_user() 函数登录用户，创建用户会话,记住用户已登录
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))









"""
Blueprint 是 Flask 框架中的一个重要特性,可以理解为应用的一个组成部分或者子模块。它的主要作用是帮助开发者组织和管理大型 Flask 应用中的路由。
具体来说:
1 功能划分: Blueprint 允许你将应用的不同功能分开。例如,你可以有一个用于用户认证的 Blueprint,另一个用于主要功能的 Blueprint。
2 代码组织: 它帮助你更好地组织代码。每个 Blueprint 可以放在单独的 Python 文件或文件夹中,使项目结构更清晰。
3 URL 前缀: 你可以为 Blueprint 设置 URL 前缀。例如,所有与认证相关的路由都可以以 "/auth" 开头。
4 模板和静态文件: Blueprint 可以有自己的模板和静态文件目录,方便管理。
5 可重用性: 你可以在多个项目中重复使用同一个 Blueprint。
对于初学者来说,你可以把 Blueprint 想象成一个小型的、独立的应用模块,它可以包含自己的路由、视图函数、模板等,但又可以很方便地集成到主应用中。
"""
