import pandas as pd
from flask import Flask, render_template
import requests as rs
from io import StringIO
from serve import *
app = Flask(__name__)

@app.route('/')
def home():
    club_list = get_home_page_club_list()
    return render_template('templates/home.html', clubs=club_list)

@app.route('/club/<id>')
def club(id):
    club_dict = get_club_from_id(id)
    return render_template('templates/club.html', club=club_dict)


if __name__ == '__main__':
    app.run(port=1090)