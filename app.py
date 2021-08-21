from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = ['Section 1', 'Section 2', 'Section 3']


@app.context_processor
def main_menu():
    return dict(
        menu=[{'name': 'Index', 'url': '/'},
              {'name': 'Hey', 'url': '/hey'},
              {'name': 'Login', 'url': '/login'}],
        path=request.url
    )


@app.route('/')
def index():  # put application's code here
    print(url_for('index'))
    return render_template('index.html')


@app.route('/hey')
def hey():
    print(url_for('hey'))
    return render_template('hey.html', title='hey')


@app.route('/login', methods=['post', 'get'])
def login():
    print(url_for('login'))
    return render_template('login.html', title='LogIn')


if __name__ == '__main__':
    app.run()
