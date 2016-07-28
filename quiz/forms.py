from flask_wtf import Form
from wtforms import (SelectField, SubmitField, SelectMultipleField,
                     validators, widgets)
from quiz.models import Quiz, Choice


class QuizForm(Form):
    choices = SelectMultipleField('Choices', coerce=int, choices=[],
                                  widget=widgets.ListWidget(prefix_label=False),
                                  option_widget=widgets.CheckboxInput())
    submit = SubmitField('Submit Answer')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices_list = Choice.query.filter_by(quiz_id=kwargs['qid']).all()
        self.choices.choices = [(choice.id, choice.content)
                                 for choice in choices_list]
        self.choices.name = 'quiz_{}'.format(kwargs['qid'])


class MultiQuizForm(Form):
    choices = []
    submit = SubmitField('Submit Answer')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.quiz_list = Quiz.query.filter(Quiz.id.in_(kwargs['qids'])).all()
        for quiz in self.quiz_list:
            self.choices.append(SelectMultipleField('Choices', coerce=int, choices=[],
                                          widget=widgets.ListWidget(prefix_label=False),
                                          option_widget=widgets.CheckboxInput()))
            for choices in self.choices:
                choices.choices.extend([(choice.id, choice.content)
                                         for choice in quiz.choices])
                # choices.name = 'quiz_{}'.format(quiz.id)
