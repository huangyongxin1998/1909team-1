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
        # 实现注册功能， 获取表单数据，增加
        grade = request.form.get('reader_grade')
        name = request.form.get('reader_name')
        pwd = request.form.get('reader_pwd')
        phone = request.form.get('reader_phone')
        print(f'级别:{grade},名字{name},密码：{pwd},电话：{phone}')
        reader = Reader(reader_name=name,reader_pass=pwd,phone=phone,grand_id=grade)
        db.session.add(reader)
        db.session.commit()
        return render_template('/index.html')



