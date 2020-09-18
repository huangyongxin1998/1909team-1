from flask import Blueprint,render_template

zhouzy = Blueprint('zhouzy',__name__)

@zhouzy.route('/')
def index():
    return render_template('/zzy/index.html')
