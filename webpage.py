from flask import Flask, render_template
from config import cfg

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    content = cfg['webpage']
    return render_template("index.html", content=content)
