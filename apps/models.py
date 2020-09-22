'''
如果是团队开发：
最快方案： 项目经理把models写完！个人按照自己需求微调！！！
'''
from config import  db # 导入数据库对象

class ReaderGrade(db.Model):
    '''读者等级表'''
    __tablename__ = "reader_grade" #表名
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #id 主键自增
    grand_name = db.Column(db.String(50),nullable=True) # 级别名字
    quan_tity =db.Column(db.Integer,nullable=True) # 可借数量2本
    max_maney = db.Column(db.Float(),nullable=True)  # 最大金额/押金
    date_amount = db.Column(db.Integer,nullable=True) # 还书期限
    #
    '''
    作者1--N书
    Author：books = db.relationship('Book', backref='author')
    Book:author_id = db.Column(db.Integer,db.ForeignKey('authors.id')) #或者是, Author.id
    '''
    # 读者返回来引用 级别
    readers =db.relationship('Reader', backref='grade')#指定读者对象，引用级别的别名！

    def to_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "id": self.id,
            "grand_name": self.grand_name,
            "quan_tity": self.quan_tity,
            "max_maney": self.max_maney,  # 押金()
            "date_amount":self.date_amount #还书期限
        }
        return user_dict

class Reader(db.Model):
    '''读者等级表'''
    __tablename__ = "reader" #表名
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #id 主键自增
    reader_name = db.Column(db.String(50),nullable=False) # 用户名
    reader_pass = db.Column(db.String(50),nullable=False)  # 用户密码
    reader_credit = db.Column(db.Integer,nullable=True) # 用户信誉度
    address = db.Column(db.String(50), nullable=True)  # 地址
    phone = db.Column(db.String(11), nullable=True)  # 电话
    is_activate =db.Column(db.Integer,nullable=True) #0表示注册未激活    1表示激活账号，已经使用过账号
    '''
        参考
       作者1--N书
       Author：books = db.relationship('Book', backref='author')
       Book:author_id = db.Column(db.Integer,db.ForeignKey('authors.id')) #或者是, Author.id
    '''
    grand_id = db.Column(db.Integer,db.ForeignKey('reader_grade.id')) # 外键表名.id


    def to_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "id": self.id,
            "reader_name": self.reader_name, # 用户名
            "reader_char": self.reader_char,# 用户名首字符
            "reader_pass": self.reader_pass, # 用户密码
            "reader_credit":self.reader_credit,# 用户信誉度
            "address": self.address,# 地址
            "phone": self.phone# 电话
        }
        return user_dict

#图书类别 BookType
class BookType(db.Model):
    '''读者等级表'''
    __tablename__ = "book_type" #表名
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #id 主键自增
    type_name = db.Column(db.String(50),nullable=True) # 级别名字
    # 读者返回来引用 级别
    readers =db.relationship('Book', backref='booktype')#指定读者对象，引用级别的别名！
    def __str__(self):
        return self.type_name

class Book(db.Model):
    '''读者等级表'''
    __tablename__ = "book" #表名
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #id 主键自增
    book_name = db.Column(db.String(50),nullable=False) # 用户名
    book_quantity = db.Column(db.Integer,nullable=False)  # 书籍数量
    bookInfo = db.Column(db.String(100),nullable=True) # 书籍说明
    book_imgsrc = db.Column(db.String(50), nullable=True)  # 书籍封面
    author = db.Column(db.String(50), nullable=True)  # 作者名字
    price = db.Column(db.Integer,nullable=True) # 单价
    bookConcern = db.Column(db.String(50), nullable=True)  # 出版社
    bookOutCount =db.Column(db.Integer,nullable=True) #出租次数
    bookChar = db.Column(db.String(10), nullable=True)  # 书籍首字母
    book_type= db.Column(db.Integer,db.ForeignKey('book_type.id')) # 外键表名.id

    def __str__(self):
           return self.book_name