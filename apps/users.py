# 用户模块
from flask import Blueprint,render_template,request,session
from .models import  Reader,ReaderGrade,Book,BookType,BookManager # 项目中一定使用一下模型类！ 否则无法迁移！
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
        reader = Reader(reader_name=name,reader_pass=pwd,phone=phone,grand_id=grade,is_activate=0) #默认未激活！
        db.session.add(reader)
        db.session.commit()
        return render_template('/index.html')



@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('index.html')
    else:
        # 1. 获取资料
        role_id= request.form.get('role_id')
        user_name = request.form.get('user_name')
        user_pwd = request.form.get('user_pwd')
        print(f'roleid:{role_id},name:{user_name},pwd:{user_pwd}')
        # 2.判断角色
        print(type(role_id))
        if role_id =="1":
            #读者用户名和密码
            reader = Reader.query.filter_by(reader_name=user_name,reader_pass=user_pwd).all()
            print(reader)
            #print(f'名字:{reader.reader_name},电话:{reader.phone}')
            #用户登录后，用户资料写入session缓存中，方便在任意页面使用！
            if len(reader)==0:
                return render_template('index.html', msg='用户名或密码错误！')
            else:
                # 用户登录成功,用户对象保存到session中,方便其他方法调用！
                session["user_id"] = reader[0].id
                session["user_name"] = reader[0].reader_name
                if reader[0].is_activate == 0:
                    msg = '请修改密码！'
                return render_template('reader.html', msg=reader[0].reader_name)
        else:
            # 系统管理员,图书管理员
            print(f'管理员名:{user_name},密码:{user_pwd}')
            manager = BookManager.query.filter_by(manage_name=user_name, manage_pass=user_pwd).all()
            if len(manager) == 0:
                return render_template('index.html', msg='管理员名或密码错误！')
            else:
                session["user_id"] = manager[0].id
                session["user_name"] = manager[0].manage_name
                if role_id =="2":
                    return render_template('bookManager.html', msg=manager[0].manage_name)
                else:
                    return render_template('systemManager.html', msg=manager[0].manage_name)




@users.route('/userinfo', methods=['GET'])
def user_info():
    '''根据id，或用户名查询，展示用户资料'''
    id = session.get('user_id')
    print(f'用户id:{id}')
    reader = Reader.query.filter_by(id=id).all()
    if len(reader)>0:
        return render_template('update_pwd.html', reader=reader[0])
    else:
        return render_template('reader.html',msg='查询无结果！')

@users.route('/updatepwd', methods=['GET','POST'])
def update_pwd():
    if request.method=='GET':
        return render_template('update_pwd.html')
    else:
        # 1.获取数据，2，完整性判断 3.修改
        old_pwd = request.form.get('old_pwd')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')

        id = session.get('user_id')
        reader = Reader.query.filter_by(id=id).first()

        # 判断
        if  not  all([old_pwd,pwd1,pwd2]): # 判断列表中的所有变量是否都有值！ 都有值返回true
            msg = '字段不能为空'
            return  render_template('update_pwd.html',msg=msg)
        else:
            # 判断用户名是否正确，两次密码是否相等
            if reader.reader_pass !=old_pwd:
                msg = '密码输入错误！'
                return render_template('update_pwd.html', msg=msg,old_pwd=old_pwd,pwd1=pwd1,pwd2=pwd2)
            if pwd1 != pwd2:
                msg = '密码不一致！'
                return render_template('update_pwd.html', msg=msg,old_pwd=old_pwd,pwd1=pwd1,pwd2=pwd2)
            try:
                reader.reader_pass = pwd2
                db.session.commit()
                return render_template('reader.html', msg='修改成功')
            except Exception as e:
                msg = '修改失败'
                return render_template('reader.html', msg='修改失败')



@users.route('/booklist', methods=['GET'])
def book_list():
    # 图书数量大于1的表示可借
    books = Book.query.filter(Book.book_quantity > 1).all()
    return render_template('book.html',books=books)




@users.route('/logout', methods=['GET'])
def logout():
    # 1.清空session中数据，跳转
    session.clear()
    return render_template('index.html')