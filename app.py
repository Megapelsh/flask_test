from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qovbqiybqvi84vbq3v3tllat4'


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


@app.route('/login', methods=['POST', 'GET'])
def login():
    print(url_for('login'))

    if request.method == 'POST':
        print(request.form)
        print(request)
        if request.form['email'] and len(request.form['password']) >2:
            flash('Login success')
        else:
            flash('Yoy need to fill all the fields correctly')
    return render_template('login.html', title='LogIn')


if __name__ == '__main__':
    app.run()
