# 书籍管理模块
from flask import Blueprint,render_template,request,session
from .models import  Reader,ReaderGrade,Book,BookType # 项目中一定使用一下模型类！ 否则无法迁移！
from  config import  db
book = Blueprint('book',__name__)

@book.route('/')
def index():
    return render_template('/bookManager.html')

@book.route('/managerinfo',methods=['GET','POST'])
def manager_info():
    return render_template('manager_info.html')