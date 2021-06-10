from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def page():
    return render_template("index.html")
    
    if __name__== '_main_':
    app.run()