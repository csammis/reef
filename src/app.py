from flask import Flask, url_for, render_template
import endpoints

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

endpoints.register(app)

@app.route('/')
def index():
    return render_template('index.html', title='Reef')

@app.route('/parameters/')
def parameters():
    return render_template('parameters.html',
            title='Parameters',
            libraries=['jquery','d3','jquery-ui'],
            stylesheet=url_for('static', filename='parameters.css'),
            script=url_for('static', filename='parameters.js'))

@app.route('/parameters/add/')
def add_parameters():
    return render_template('add_parameters.html')

@app.route('/logs/')
def logs():
    return render_template('logs.html',
            title='Logs',
            libraries=['jquery','jquery-ui'],
            stylesheet=url_for('static', filename='logs.css'),
            script=url_for('static', filename='logs.js'))

@app.route('/settings/')
def settings():
    return render_template('settings.html',
            title='Settings',
            libraries=['jquery'],
            stylesheet=url_for('static', filename='settings.css'),
            script=url_for('static', filename='settings.js'))

if __name__ == '__main__':
    app.run(debug=True)

