from flask import Blueprint,render_template

xufeiyu = Blueprint('xufeiyu',__name__)

@xufeiyu.route('/')
def index():
    return render_template('/xfy/xfyindex.html')
