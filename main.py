import pandas as pd
from flask import Flask, render_template
import requests as rs
from io import StringIO
from serve import *
app = Flask(__name__)

@app.route('/')
def home():
    club_list = get_home_page_club_list()
    return render_template('home.html', clubs=club_list)

@app.route('/club/<id>')
def club(id: int):
    try: id = int(id)
    except: return '404'
    club_dict = get_club_from_id(id)
    return render_template('club.html', club=club_dict)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/event/<club_id>/<event_id>')
def event(club_id: int, event_id: int):
    return render_template('')

if __name__ == '__main__':
    app.run(port=1090)