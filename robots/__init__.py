from datetime import datetime

from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, RadioField
from wtforms.validators import DataRequired

from sqlalchemy.sql.functions import count, max

from .db import SESSION, Game

app = Flask(__name__)


@app.route('/')
def index():
    s = SESSION()
    """
    select user, max(date), count(user) from game order by date group by user"""
    qs = s.query(Game.user, max(Game.date).label('recent'), count(Game.user).label('wins')).filter(Game.date > datetime.now().replace(day=1)).group_by(Game.user).all()
    print(qs)
    return render_template('leaderboard.html', users=qs, game_url=url_for('.new_game'))


@app.route('/game', methods=['GET', 'POST'])
def new_game():
    form = RobotsForm(csrf_enabled=False)
    print('Gonna validate now')
    if request.method == 'POST' and form.validate():
        print('Validation success')
        print(form.user.data)
        s = SESSION()
        s.add(Game(**form.data))
        s.commit()
        s.close()
        return index()
    return render_template('game_entry.html', form=form, leaderboard_url=url_for('.index'))


class RobotsForm(FlaskForm):
    user = StringField('user', validators=[DataRequired()])
    color = RadioField('color', choices=[('red', 'red'), ('yellow', 'yellow'), ('blue', 'blue'), ('green', 'green')],
                       validators=[DataRequired()])
    pre_moved = BooleanField('pre_moved', default=False)
    symbol = StringField('symbol')
    other_colors_pre_moved = BooleanField('other_colors_pre_moved', default=False)
    other_colors_moved = BooleanField('other_colors_moved', default=False)
    date = DateTimeField('date', default=datetime.now())
