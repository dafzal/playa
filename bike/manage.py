# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask.ext.script import Command
from flask.ext.script import Manager, Server
from bike import app
from bike.models import Bike, Renter
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=80)
)

from csv import DictReader
class Data(Command):
  def run(self):
    print 'running data'
    from bike import db
    reader = DictReader(open('data.csv','r').readlines())
    for r in reader:
      r = {k: v.decode('utf8','ignore') for k, v in r.iteritems()}
      db.add(Renter(name=r['Billing Name'], 
        email=r['Email'], desc=r['Lineitem name'], qty=r['Quantity'], 
        zipcode=r['Billing Zip'], phone=r['Billing Phone']))

    for i in xrange(1000):
      db.add(Bike(code=str(i)))
    try:
      db.commit()
    except:
      pass
    import ipdb
    ipdb.set_trace()
    print 'done'

manager.add_command('data', Data())

if __name__ == "__main__":
  manager.run()