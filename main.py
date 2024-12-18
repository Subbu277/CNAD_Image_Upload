from flask import Flask
from apis import upload_api,health_api,ui_api

app = Flask(__name__)

app.register_blueprint(upload_api)
app.register_blueprint(health_api)
app.register_blueprint(ui_api)



if __name__ == '__main__':
    app.run(port=8080, debug=True)
