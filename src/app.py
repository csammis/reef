""" Flask app configuration and definition """
from flask import Flask, url_for, render_template, redirect
import endpoints
from models import has_minimum_setup

app = Flask(__name__)

# Jinja setup
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.tests['is_true'] = lambda value: value is True

endpoints.register(app)

@app.route('/')
def index():
    """ A root index page """
    if has_minimum_setup() is False:
        return redirect(url_for('setup'))

    return render_template('index.html', title='Reef')

@app.route('/setup/')
def setup():
    """ Setup landing page for an unconfigured install """
    if has_minimum_setup():
        return redirect(url_for('settings'))

    return render_template('setup.html',
                           title='Welcome and setup',
                           libraries=['jquery', 'jquery-ui'],
                           stylesheet=url_for('static', filename='setup.css'),
                           script=url_for('static', filename='setup.js'))

@app.route('/parameters/')
def parameters():
    """ Display and editing of tank parameters """
    if has_minimum_setup() is False:
        return redirect(url_for('setup'))

    return render_template('parameters.html',
                           title='Parameters',
                           libraries=['jquery', 'd3', 'jquery-ui'],
                           stylesheet=url_for('static', filename='parameters.css'),
                           script=url_for('static', filename='parameters.js'))

@app.route('/logs/')
def logs():
    """ Display and editing of tank changelogs """
    if has_minimum_setup() is False:
        return redirect(url_for('setup'))

    return render_template('logs.html',
                           title='Logs',
                           libraries=['jquery', 'jquery-ui'],
                           stylesheet=url_for('static', filename='logs.css'),
                           script=url_for('static', filename='logs.js'))

@app.route('/schedules/')
def schedules():
    """ An outer page to access tank schedules """
    if has_minimum_setup() is False:
        return redirect(url_for('setup'))

    return render_template('schedules.html',
                           title='Schedules',
                           libraries=['jquery', 'jquery-ui'],
                           stylesheet=url_for('static', filename='schedules.css'),
                           script=url_for('static', filename='schedules.js'))

@app.route('/schedules/<tank_name>/')
def schedules_for_tank(tank_name):
    """ Individual inner page for a specific tank's schedule """
    if has_minimum_setup() is False:
        return redirect(url_for('setup'))

    tank = endpoints.config_manager.get_tank_from_name(tank_name)
    if tank is None:
        return '?', 404

    return render_template('schedules.html',
                           tank_name=tank_name,
                           schedule=endpoints.config_manager.get_scheduled_events(tank.id))

@app.route('/settings/')
def settings():
    """ Settings and configuration """
    if has_minimum_setup() is False:
        return redirect(url_for('setup'))

    return render_template('settings.html',
                           title='Settings',
                           libraries=['jquery', 'jquery-ui'],
                           stylesheet=url_for('static', filename='settings.css'),
                           script=url_for('static', filename='settings.js'))

if __name__ == '__main__':
    app.run(debug=True)

