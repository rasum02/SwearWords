from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

from GreenGroceries.utils.choices import LanguageChoices, WordCategoryChoices, CountryChoices


class FilterWordsForm(FlaskForm):
    word = StringField('Word',
                       render_kw=dict(placeholder='Search for a swearword...'))
    language = SelectField('Language',
                           choices=[('', 'All languages')] + LanguageChoices.choices())
    category = SelectField('Category',
                           choices=[('', 'All categories')] + WordCategoryChoices.choices())
    country = SelectField('Country',
                          choices=[('', 'All countries')] + CountryChoices.choices())
    submit = SubmitField('Search')
