# create_app 是一个工厂函数,用于创建和配置 Flask 应用实例，db 是一个 SQLAlchemy 数据库实例
from app import create_app, db

app = create_app()

# 常见的 Python 惯用法,确保只有在直接运行此脚本时,下面的代码才会执行。
# 如果这个文件被导入为模块,下面的代码不会执行。
if __name__ == '__main__':
    
    # 创建了一个应用上下文。在这个上下文中,可以访问当前应用的配置和资源。
    with app.app_context():

        # 用于创建数据库表。它会根据你的模型定义创建所有必要的表格。
        db.create_all()

    # 启动 Flask 开发服务器,并启用调试模式。
    # 在调试模式下,服务器会在代码变更时自动重启,并在发生错误时显示详细的错误信息。
    app.run(debug=True)
