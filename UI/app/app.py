from flask import Flask
app = Flask("CHLEN")

@app.route('/')
def hello_world():
  return '<h1>ПЕНИС</h1>'

app.run(debug=True)