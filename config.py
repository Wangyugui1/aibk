import os    # 提供了与操作系统交互的功能,如访问环境变量和处理文件路径。
from dotenv import load_dotenv    #  dotenv库用于从.env文件加载环境变量。

load_dotenv()    #  读取当前目录下的.env文件(如果存在),并将其中定义的变量加载到环境中。

#  Config类集中了应用程序的各种设置,使用环境变量来存储敏感信息(如密钥和数据库URL),
#  这样可以更安全地管理这些信息,并且便于在不同环境(如开发、测试、生产)之间切换配置。
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
    
