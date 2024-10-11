from flask import Flask
from apis import upload_api,health_api,ui_api
import os

app = Flask(__name__)

app.register_blueprint(upload_api)
app.register_blueprint(health_api)
app.register_blueprint(ui_api)



if __name__ == '__main__':
    tmp_dir = "tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    app.run(port=8080, debug=True)
