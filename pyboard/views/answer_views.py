from flask import Blueprint, url_for,request, render_template, g,flash
from datetime import datetime
from werkzeug.utils import redirect
from pyboard.models import Question,Answer
from pyboard import db
from pyboard.forms import AnswerForm
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>',methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    q = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        a = Answer(content=content, create_date = datetime.now(),user=g.user)
        q.answer_set.append(a)
        db.session.commit()
        return redirect(url_for('question.detail',question_id=question_id))
    return render_template('question/question_detail.html',question=q, form=form)

@bp.route('/modify/<int:answer_id>',methods=('GET','POST'))
@login_required
def modify(answer_id):
    a = Answer.query.get_or_404(answer_id)
    if g.user != a.user:
        flash('수정 권한이 없습니다!')
        return redirect(url_for('question.detail',question_id=a.question.id))
    if request.method == 'POST':
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(a)
            a.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id= a.question.id))
    else:
        form = AnswerForm(obj=a)
    return render_template('answer/answer_form.html',answer=a ,form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    a = Answer.query.get_or_404(answer_id)
    q_id = a.question.id
    if g.user != a.user:
        flash('삭제 권한이 없습니다!')
    else:
        db.session.delete(a)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=q_id))