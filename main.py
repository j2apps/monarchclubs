from flask import Flask, render_template
from modules.serve import *
from modules.updates import *
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# Set scheduler time zone
scheduler = BackgroundScheduler(timezone="America/Denver")
# Updates clubs every hour
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=run_checks,
    trigger="cron",
    max_instances=1,
    hour='*'
)
# Runs from Monday to Friday at 8:30 (am)
'''scheduler.add_job(
    func=send_email,
    trigger="cron",
    max_instances=1,
    day_of_week='mon-fri',
    hour=8,
    minute=30
)'''
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