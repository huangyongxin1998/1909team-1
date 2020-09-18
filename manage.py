from flask import  Flask,render_template
from config import  create_app,db  #配置文件中
from flask_script import Manager # 扩展db指令
from flask_migrate import  Migrate,MigrateCommand # 数据库迁移库
from apps.models import Reader,ReaderGrade # 导入模型类
app = create_app()
manager = Manager(app) # 命令管理类
migrate = Migrate(app,db=db) #创建迁移对象
manager.add_command('db',MigrateCommand)  #扩展新的数据库操作指令db

if __name__ == '__main__':
    manager.run() #启动