from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
@main.route('/home')
def homepage():
    return render_template('home.html', active_menu=0)
