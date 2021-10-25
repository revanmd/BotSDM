from flask import Flask

def init_app(config_name):
	app = Flask(__name__,instance_relative_config=False)
	app.config.from_object(config_name)

	with app.app_context():
		from .api import api

		app.register_blueprint(api, url_prefix='/api')	
		
		return app