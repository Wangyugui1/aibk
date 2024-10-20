# AIKB (AI Knowledge Base)

AIKB 是一个基于 Flask 的人工智能知识库系统,旨在帮助用户管理和查询文档。本项目提供了一个用户友好的界面,支持文件上传、AI 查询等功能。

[点击体验](https://aikb.yuguiwang.me/)

## 功能特点

- 用户认证系统(注册、登录、登出)
- 文件上传和管理
- 基于 AI 的文档查询
- 响应式设计,支持移动设备

## 技术栈

- 后端: Python, Flask
- 前端: HTML, CSS, JavaScript, Bootstrap
- 数据库: MySQL
- Web服务器: Nginx
- WSGI服务器: Gunicorn

## 项目结构

```
AIKB/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   └── js/
│   │       └── main.js
│   └── templates/
│   |   ├── base.html
│   |   ├── index.html
│   |   ├── login.html
│   |   ├── register.html
│   |   └── dashboard.html
|   |___uploads
├── config.py
├── requirements.txt
|——— run.py
|————.env
```


## 使用方法

1. 注册一个新账户或登录现有账户。
2. 在仪表板页面,您可以上传新文件或查看已上传的文件。
3. 使用 AI 查询功能来搜索和分析您的文档。

## 部署步骤

### 1. 环境准备

- 安装 Python 3.10 或更高版本
- 安装 MySQL 8.0 或更高版本
- 安装 Nginx

### 2. 数据库设置

1. 登录 MySQL:
   ```
   mysql -u root -p
   ```

2. 创建数据库和用户:
   ```sql
   CREATE DATABASE aikb;
   CREATE USER 'aikb_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON aikb.* TO 'aikb_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```
   注意: 请将 'your_password' 替换为您自己设置的安全密码。

### 3. 项目设置

1. 克隆项目:
   ```
   git clone https://github.com/Wangyugui1/aibk.git
   cd aibk
   ```

2. 创建虚拟环境:
   ```
   python -m venv aikb_env
   source aikb_env/bin/activate  # 在 Windows 上使用 aikb_env\Scripts\activate
   ```

3. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

4. 配置环境变量:
   创建 `.env` 文件并添加以下内容:
   ```
   DATABASE_URL=mysql+pymysql://aikb_user:your_password@localhost/aikb
   SECRET_KEY=your_secret_key
   ```
   注意: 请将 'your_password' 和 'your_secret_key' 替换为实际值。

5. 初始化数据库:
   ```
   flask db upgrade
   ```

### 4. Gunicorn 设置

1. 安装 Gunicorn:
   ```
   pip install gunicorn
   ```

2. 创建 `gunicorn.conf.py`:
   ```python
   workers = 3
   bind = "127.0.0.1:8002"
   timeout = 120
   ```

### 5. Nginx 设置

1. 创建 Nginx 配置文件:
   ```
   sudo nano /etc/nginx/sites-available/aikb
   ```

2. 添加以下内容:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8002;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   注意: 将 'your_domain.com' 替换为您的实际域名。

3. 启用站点:
   ```
   sudo ln -s /etc/nginx/sites-available/aikb /etc/nginx/sites-enabled
   ```

4. 测试 Nginx 配置:
   ```
   sudo nginx -t
   ```

5. 重启 Nginx:
   ```
   sudo systemctl restart nginx
   ```

### 6. 启动应用

1. 启动 Gunicorn:
   ```
   nohup gunicorn -c gunicorn.conf.py run:app &
   ```

2. 确保防火墙允许 HTTP 流量:
   ```
   sudo ufw allow 'Nginx Full'
   ```

## 维护

- 查看日志: `tail -f nohup.out`
- 重启应用:
  ```
  pkill gunicorn
  nohup gunicorn -c gunicorn.conf.py run:app &
  ```

## 注意事项

- 定期备份数据库
- 保持系统和依赖包更新
- 监控服务器资源使用情况

## 贡献

欢迎提交问题和拉取请求。对于重大更改,请先开issue讨论您想要更改的内容。

## 许可证

本项目采用 [Apache 2.0 许可证](LICENSE)。
