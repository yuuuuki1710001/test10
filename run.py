from flask import Flask
from cookme import Component1, Component2, upload

app = Flask(__name__)
app.register_blueprint(Component2.user)
app.register_blueprint(Component1.cookme)
app.register_blueprint(upload.img)
app.config['SECRET_KEY'] = 'recipe key'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
