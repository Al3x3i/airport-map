from flask import Flask
from flask_cors import CORS
#import socket
import os

from controller import blueprint
from elasticsearchUtils import ElasticsearchUtils

# Initialize Elasticsearch
ES_DEFAULT_PORT = 9200
# Optinally: the network name is defined by --name es_db, check README.md
ES_DEFAULT_HOST = 'localhost'

APP_DEFAULT_PORT = 5000
APP_DEFAULT_HOST = '0.0.0.0'
APP_DEBUG_MODE = False


# Define automatically elasticsearch connection HOST. Be sure the elasticsearch is active, otherwise
# it might not find it if then elasticsearch run in parallel
# s = socket.socket()
# try:
#     s.connect((ES_DEFAULT_HOST, ES_DEFAULT_PORT))
# except Exception as e:
#     ES_DEFAULT_HOST = 'localhost'
# finally:
#     s.close()


# if len(sys.argv) == 0:
#     ELASTICSEARCH_HOST = os.environ.get("es", sys.argv[0])
# else:
#     ELASTICSEARCH_HOST = os.environ.get("es", DEFAULT_HOST)


ES_DEFAULT_CONNECTION_RETRIES = 3

es_con_host = os.environ.get(
    "ES_HOST", ES_DEFAULT_HOST)
es_con_retries = os.environ.get(
    "ES_RETRY_CONNECTIONS", ES_DEFAULT_CONNECTION_RETRIES)

print("Elasticsearch connection %s:%d." %
      (es_con_host, ES_DEFAULT_PORT))

utils = ElasticsearchUtils(el_host=es_con_host, el_port=ES_DEFAULT_PORT,
                           es_connection_retries=int(es_con_retries))


def create_app():
    # The build_webapp is generated buy npm run build
    app = Flask(__name__, static_folder='./static',
                template_folder="./build_template")
    CORS(app)
    app.config.from_object("config.DevelopmentConfig")
    app.register_blueprint(blueprint)
    app.el_utils = utils
    app.run(host=APP_DEFAULT_HOST, port=APP_DEFAULT_PORT)


if __name__ == '__main__':
    utils.initialize_elasticsearch()
    create_app()
