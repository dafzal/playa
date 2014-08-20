from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask

engine = create_engine('sqlite:///test.db', convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=False,
                     autoflush=False,
                     bind=engine))
Base = declarative_base()
Base.query = db.query_property()
app = Flask(__name__)


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX 123R~XHH!jmN]LWX/,?RT'
@app.teardown_appcontext
def shutdown_session(exception=None):
  db.remove()

from bike.models import Bike, Renter
print 'creating engine'
Base.metadata.create_all(bind=engine)
from bike.views import *
if __name__ == '__main__':
    app.run(port=80)