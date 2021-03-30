from flask import Blueprint, render_template, url_for, request, g, flash
from pyboard.models import Question
from datetime import datetime
from werkzeug.utils import redirect
from pyboard import db
from pyboard.forms import QuestionForm,AnswerForm
from pyboard.views.auth_views import login_required

bp = Blueprint('question',__name__,url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page',type=int,default=1)
    q_list = Question.query.order_by(Question.create_date.desc())
    q_list = q_list.paginate(page,per_page=20)
    return render_template('question/question_list.html', question_list = q_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    q = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question = q, form = form)

@bp.route('/create/',methods=('GET','POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        q = Question(subject = form.subject.data,content =form.content.data,
                     create_date=datetime.now(), user=g.user)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form = form)

@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required
def modify(question_id):
    q = Question.query.get_or_404(question_id)
    if g.user != q.user:
        flash('수정 권한이 없습니다!')
        return redirect(url_for('question.detail',question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(q)
            q.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id= question_id))
    else:
        form = QuestionForm(obj=q)
    return render_template('question/question_form.html', form=form)


@bp.route('/delete//<int:question_id>')
@login_required
def delete(question_id):
    q = Question.query.get_or_404(question_id)
    if g.user != q.user:
        flash('삭제 권한이 없습니다!')
        return redirect(url_for('question.detail',question_id=question_id))
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for('question._list'))

