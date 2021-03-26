from flask import Blueprint, url_for,request, render_template
from datetime import datetime
from werkzeug.utils import redirect
from pyboard.models import Question,Answer
from pyboard import db
from pyboard.forms import AnswerForm

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>',methods=('POST',))
def create(question_id):
    form = AnswerForm()
    q = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        a = Answer(content=content, create_date = datetime.now())
        q.answer_set.append(a)
        db.session.commit()
        return redirect(url_for('question.detail',question_id=question_id))
    return render_template('question/question_detail.html',question=q, form=form)