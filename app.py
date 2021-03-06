"""
    app     :   C1, C2, upload接続処理
    Date    :   2020/07/21
    Purpose :   C1, C2, uploadをBlueprintで接続する
"""

import os
from flask import Flask
from cookme import Component1, Component2, upload

app = Flask(__name__)
app.register_blueprint(Component2.user)
app.register_blueprint(Component1.cookme)
app.register_blueprint(upload.img)
app.config['SECRET_KEY'] = 'recipe key'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
