from app import create_app
from flask import render_template

app = create_app()

# This is the "Master Route" - it will force localhost:5000 to work
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)