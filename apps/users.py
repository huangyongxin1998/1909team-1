# 用户模块
from flask import Blueprint,render_template,request
from .models import  Reader,ReaderGrade # 项目中一定使用一下模型类！ 否则无法迁移！
from  config import  db
users = Blueprint('users',__name__)

@users.route('/')
def index():
    return render_template('/index.html')



@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='GET':
        return render_template('/register.html')
    else:
        return render_template('/index.html')
