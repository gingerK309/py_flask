from flask import Blueprint, render_template, url_for, request
from pyboard.forms import QuestionForm
from pyboard.models import Question
from datetime import datetime
from werkzeug.utils import redirect
from pyboard import db
from pyboard.forms import QuestionForm,AnswerForm

bp = Blueprint('question',__name__,url_prefix='/question')

@bp.route('/list/')
def _list():
    q_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list = q_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    q = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question = q, form = form)

@bp.route('/create/',methods=('GET','POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        q = Question(subject = form.subject.data,content =form.content.data,
                     create_date=datetime.now())
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form = form)