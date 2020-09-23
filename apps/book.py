# 书籍管理模块
from flask import Blueprint,render_template,request,session
from .models import  Reader,ReaderGrade,Book,BookType,BookManager # 项目中一定使用一下模型类！ 否则无法迁移！
from  config import  db
book = Blueprint('book',__name__)

@book.route('/')
def index():
    return render_template('/bookManager.html')

@book.route('/managerinfo/<int:num>',methods=['GET','POST'])
def manager_info(num):
    if request.method=='GET':
        id = session.get("user_id")
        print(f'管理员id:{id}')
        #return render_template('manager_info.html')

        manager =BookManager.query.filter_by(id=id).all()
        if len(manager) >0:
            return render_template('manager_info.html',manager=manager[0],num=num)
    else:
        # 1. 获取资料,先查,再改 -->db.session.commit()
        id = request.form.get('id')
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        address =  request.form.get('address')
        phone = request.form.get('phone')
        print(f'id:{id},名字:{name}')
        m1=  BookManager.query.get(id)
        print('当前用户......')
        m1.manage_name= name
        m1.manage_pass = pwd
        m1.address = address
        m1.phone= phone
        db.session.commit()
        return render_template('bookManager.html',info='修改成功')


