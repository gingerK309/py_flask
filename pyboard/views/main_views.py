from flask import Blueprint

bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/hello')
def hello():
    return 'hello'

@bp.route('/')
def index():
    return 'pyboard inedx'