from flask import Flask

#Flask Constructor
app = Flask(__name__)

#View Function -Decorator
@app.route('/index')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()    