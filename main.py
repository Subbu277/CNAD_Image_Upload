from flask import Flask
from apis import upload_api,health_api,ui_api
import os
import logging

app = Flask(__name__)

app.register_blueprint(upload_api)
app.register_blueprint(health_api)
app.register_blueprint(ui_api)



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    tmp_dir = "tmp"
    logger.info("Checking if tmp directory exists: %s", os.path.exists(tmp_dir))

    if not os.path.exists(tmp_dir):
        logger.info("Creating tmp directory")
        os.makedirs(tmp_dir)

    logger.info("tmp directory is present")
    app.run(port=8080, debug=True)
