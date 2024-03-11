from flask import Flask, render_template
from modules.serve import *
from modules.club_updates import *
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# updates clubs every hour
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_club_updates, trigger="interval", hours=1)
scheduler.start()


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


atexit.register(lambda: scheduler.shutdown())
if __name__ == '__main__':
    app.run(port=1090)