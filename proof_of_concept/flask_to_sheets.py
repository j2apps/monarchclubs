import pandas as pd
from flask import Flask, render_template
import requests as rs
from io import StringIO
app = Flask(__name__)


@app.route('/<id>')
def id_page(id):
    try:
        id = int(id)
    except:
        return('404')
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS0HMAo-BIG0kZDkZ05U8DOMSzpaeSyBkIttkwl2KVO6Ut1SE-A5rFcUAHqoqZbQ8b_KPoHZjMBDd6o/pub?output=csv'
    res = rs.get(url=url)
    s = str(res.content, 'utf-8')
    df = pd.read_csv(StringIO(s))

    club = df.iloc[id]
    a, b, c = club[['a','b','c']]
    return render_template('index.html', a=a, b=b, c=c)

if __name__ == '__main__':
    app.run(port=1090)








