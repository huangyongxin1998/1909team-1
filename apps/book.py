# 书籍管理模块
from flask import Blueprint,render_template,request,session
from .models import  Reader,ReaderGrade,Book,BookType,BookManager,BorrowBook # 项目中一定使用一下模型类！ 否则无法迁移！
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

@book.route('/readerall',methods=['GET'])
def reader_all():
    paginate = Reader.query.paginate(1, 2)  # 默认显示第1页

    # 获取页数
    page = int(request.args.get('page',1))
    if page <= 0:
        page = 1
    if page >= paginate.pages:  # 共3页, 输入30-->显示最大页3
        page = paginate.pages #最大页数

    paginate = Reader.query.paginate(page, 2)# 重新查询
    readers = paginate.items  # 当前页数据(默认是第1页数据)
    return render_template('reader_list.html',readers=readers,paginate=paginate)

@book.route('/bookall',methods=['GET'])
def book_all():
    books = Book.query.all()
    return render_template('book.html',books= books)

@book.route('/borrow_search',methods=['GET','POST'])
def borrow_search():
    if request.method=='GET':
        return render_template('book_borrow_search.html')
    else:
        # 1. 获取读者名
        reader_name = request.form.get('reader_name')
        # 2. 查询当前读者所借的书籍
        #mybooks = BorrowBook.query.filter(BorrowBook.reader.reader_name == reader_name,BorrowBook.restore_date == None).all()
        reader = Reader.query.filter_by(reader_name=reader_name).first()
        mybooks = BorrowBook.query.filter(BorrowBook.reader_id == reader.id, BorrowBook.restore_date == None).all()
        return render_template('book_borrow_search.html',books=mybooks,reader_name=reader_name,reader_id=reader.id)

@book.route('/borrow_queren',methods=['POST'])
def borrow_queren():
    allid= request.form.getlist('ck')
    manager_id = session.get('user_id')
    manager_name = session.get("user_name")
    print(f'所选书:{allid}')
    # 查书
    for id in allid:
        # 查询这本书user = User.query.get(1)
        book = BorrowBook.query.get(id)
        book.manager_id=manager_id
        db.session.commit() #修改

    return render_template('bookManager.html',manager_name=manager_name)