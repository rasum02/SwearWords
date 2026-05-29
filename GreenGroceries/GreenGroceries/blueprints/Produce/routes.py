from flask import render_template, request, Blueprint

from GreenGroceries.forms import FilterWordsForm
from GreenGroceries.queries import get_words_by_filters

Produce = Blueprint('Produce', __name__)


@Produce.route("/produce", methods=['GET', 'POST'])
@Produce.route("/swearwords", methods=['GET', 'POST'])
def produce():
    form = FilterWordsForm()
    title = 'Swear Words'
    words = []
    if request.method == 'POST':
        words = get_words_by_filters(
            word=request.form.get('word'),
            language=request.form.get('language'),
            category=request.form.get('category'),
            country=request.form.get('country')
        )
    return render_template('pages/produce.html', words=words, form=form, title=title)
