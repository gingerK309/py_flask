from flask import Flask,g, Response, make_response,request, session
from datetime import datetime,date,timedelta

app = Flask(__name__)
app.debug = True

app.config.update(
    SECRET_KEY ='notsecret',
    SESSION_COOKIE_NAME='py_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)

@app.route('/ss') #세션 설정
def ss():
    session['token'] = '123x'
    return 'session 설정'

@app.route('/gs') #세션 받기
def gs():
    return session.get('token')

@app.route('/ds') #세션 삭제
def ds():
    if session.get('token'):
        del session['token']
    return 'session 삭제'

@app.route('/wc') #쿠키 쓰기
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response('set cookie')
    res.set_cookie(key,val)
    session['token'] = '123x'
    return make_response(res)

@app.route('/rc') #쿠키 읽기
def rc():
    key = request.args.get('key')
    val = request.cookies.get(key)
    return f'cookie[{key}]={val},{session.get("token")}'

@app.route('/reqenv') #가상 환경
def reqenv():
   return  ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
        'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
        'PATH_INFO: %(PATH_INFO) s <br>'
        'QUERY_STRING: %(QUERY_STRING) s <br>'
        'SERVER_NAME: %(SERVER_NAME) s <br>'
        'SERVER_PORT: %(SERVER_PORT) s <br>'
        'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
        'wsgi.version: %(wsgi.version) s <br>'
        'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
        'wsgi.input: %(wsgi.input) s <br>'
        'wsgi.errors: %(wsgi.errors) s <br>'
        'wsgi.multithread: %(wsgi.multithread) s <br>'
        'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
        'wsgi.run_once: %(wsgi.run_once) s') % request.environ


def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str,fmt)
    return trans

@app.route('/dt') #요청 매개변수 커스텀 함수
def dt():
    datestr = request.values.get('date',date.today(),
                                 type=ymd('%Y-%m-%d'))
    return '오늘 날짜는 ' + str(datestr)

@app.route('/rp') #요청
def rp():
    # q = request.args.get('q')
    q= request.args.getlist('q')
    return 'q = %s' % str(q)


@app.route('/res1') #응답
def res1():
    custom_res = Response('custom res',201,{'test':
                                            'ttt'})
    return make_response(custom_res)

@app.route('/wsgi') #응답
def wsgi():
    def application(environ, start_response):
        body = 'the req method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type','text/plain'),('Content-Length',str(len(body)))]
        start_response('200 ok',headers)
        return [body]
    return make_response(application)

@app.before_request #요청 핸들러
def before_request():
    print('before req!')
    g.str = 'g 입니다'

@app.route('/gg') #전역 오브젝트 g
def g():
    return 'hello '+getattr(g,'str','111')

@app.route('/') #메인
def hello():
    return 'hello world!'

app.run(host='127.0.0.1')