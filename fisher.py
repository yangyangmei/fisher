import json

from app import create_app
# from flask_migrate import Migrate,MigrateCommand
# from flask_script import Shell, Manager
# from app.models.base import db

app = create_app()

# manager = Manager(app)
# migrate = Migrate(app,db)
# manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    # manager.run()

    app.run(host='0.0.0.0', debug=app.config["DEBUG"])
    # app.run(host='0.0.0.0',debug=app.config["DEBUG"], threaded=True)  # 开启多线程需要threaded设置为True