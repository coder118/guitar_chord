from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():#create_app은 플라스크 내부에서 정의된 함수명
    app = Flask(__name__)#플라스크 애플리케이션을 생성하는 코드
    
    app.config.from_object(config)

    # ORM
    # db.init_app(app)
    # migrate.init_app(app, db)
    #from . import models
    
    #flask db migrate모델을 새로 생성하거나 변경할 때 사용 (실행하면 작업파일이 생성된다.)
    #flask db upgrade모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용 (위에서 생성된 작업파일을 실행하여 데이터베이스를 변경한다.)
    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)


    return app

#https://wikidocs.net/81504
#git add . 
#git commit -m "아무거나"
#git push
#곡 제목을 입력한다. 그 곡에 적힌 코드들을 한번 쫙 확인한 후 구글링을 통해서 각 코드를 찾아내어 이미지로 추출해준다. 