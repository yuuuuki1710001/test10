from flask import Flask
from cookme import Component1, C2, upload

app = Flask(__name__)
app.register_blueprint(C2.user)
app.register_blueprint(Component1.cookme)
app.register_blueprint(upload.img)
app.config['SECRET_KEY'] = 'recipe key'

if __name__ == '__main__':
    app.run(debug=True)
