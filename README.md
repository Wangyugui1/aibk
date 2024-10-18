# AIKB 项目部署说明

### 本项目目录结构：

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

## 1. 环境准备

- 安装 Python 3.10 或更高版本
- 安装 MySQL 8.0 或更高版本
- 安装 Nginx

## 2. 数据库设置

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

   请确保将 'your_password' 替换为您设置的实际密码。

## 3. 项目设置

1. 克隆项目:
   ```
   git clone <项目仓库URL>
   cd AIKB
   ```

2. 创建虚拟环境:
   ```
   python -m venv aikb_env
   source aikb_env/bin/activate
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

5. 初始化数据库:
   ```
   flask db upgrade
   ```

## 4. Gunicorn 设置

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

## 5. Nginx 设置

1. 创建 Nginx 配置文件:
   ```
   sudo vim /etc/nginx/sites-available/aikb
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

## 6. 启动应用

1. 启动 Gunicorn:
   ```
   nohup gunicorn -c gunicorn.conf.py run:app &
   ```

2. 确保防火墙允许 HTTP 流量:
   ```
   sudo ufw allow 'Nginx Full'
   ```

## 7. 维护

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
