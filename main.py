from flask import Flask
from apis import upload_api,health_api,ui_api
import os

app = Flask(__name__)

app.register_blueprint(upload_api)
app.register_blueprint(health_api)
app.register_blueprint(ui_api)



if __name__ == '__main__':
    tmp_dir = "tmp"
    print("---------------0:",os.path.exists(tmp_dir))
    if not os.path.exists(tmp_dir):
        print("-------------1 : created tmp dir")
        os.makedirs(tmp_dir)
    print("-------------2 : tmp tmp present")
    app.run(port=8080, debug=True)
