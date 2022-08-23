from flask import Flask
from flask import request, abort, render_template

app = Flask(__name__)
@app.route('/reports/<user>')
def loadCity(user):
    browser = request.headers.get('User-Agent')
    return render_template('template.html', name = user)
if __name__ == '__main__':
    app.run(debug=True)