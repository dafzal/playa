from bike import app, db
from bike.models import Bike, Renter
from flask import request, redirect, render_template, abort
import re
from sqlalchemy import or_
from flask import jsonify

@app.route('/')
def index():
  return render_template('home.html', renters=db.query(Renter))

@app.route('/bike/<code>')
def bike(code):
  if db.query(Bike).filter_by(code=code).count():
    return render_template('bike.html', bike=db.query(Bike).filter_by(code=code)[0])
  else:
    abort(404)

@app.route('/bike/<code>', methods=['POST'])
def bike_return(code):
  bike = db.query(Bike).filter_by(code=code)[0]
  if 'comment' in request.values:
    bike.comment = request.values['comment']
  if request.values.get('return','') == 'true':
    bike.renter = None
  db.commit()
  return render_template('bike.html', bike=bike)

@app.route('/renter/<email>', methods=['GET','POST'])
def renter(email):
  if not db.query(Renter).filter_by(email=email).count():
    abort(404)
  
  renter = db.query(Renter).filter_by(email=email)[0]
  err = ''
  if 'attach_bike' in request.values:
    bike = db.query(Bike).filter_by(code=request.values['attach_bike'])[0]
    status, err = renter.attach_bike(bike)
    db.commit()

  return render_template('renter.html', renter=renter, error=err)


@app.route('/renters')
def renters():
  return render_template('renters.html', renters=db.query(Renter))

@app.route('/bikes')
def bikes():
  return render_template('bikes.html', bikes=db.query(Bike))

@app.route('/renter/<email>', methods=['POST'])
def attach_bike(email):
  if 'attach_bike' in request.values:
    renter = db.query(Renter).filter_by(email=request.values['renter'])[0]
    bike = db.query(Bike).filter_by(code=request.values['attach_bike'])[0]
    status, err = renter.attach_bike(bike)
    db.commit()
    return render_template('renter.html', renter=renter, error=err)
@app.route('/scan')
def scan():
  code = request.values['code'].strip()
  # Lookup bike serial
  if db.query(Bike).filter_by(code=code).count():
    return redirect('/bike/'+code)
  # Lookup renter code
  elif db.query(Renter).filter_by(email=code).count():
    return redirect('/renter/'+code)

  # Lookup renter email or phone
  renters = db.query(Renter).filter(or_(Renter.email.ilike(code),
                                        Renter.phone.ilike(code)))
  if renters.count() == 1:
    return redirect('/renter/'+renters[0].email)
  elif renters.count() > 1:
    return render_template('renters.html', renters=renters)
  
  # Lookup zipcode
  parts = code.split()
  all_renters = []
  if len(parts) > 1:
    for part in parts:
      zipcode = part.strip()
      name = ' '.join(x.strip() for x in parts if x != zipcode)
      print name
      print zipcode
      renters = db.query(Renter).filter(Renter.name.ilike('%'+name+'%'),
                                        Renter.zipcode.ilike('%'+zipcode+'%'))
      if renters.count() > 0:
        print 'zip found'
        all_renters += list(renters)
    if len(all_renters) == 1:
      return redirect('/renter/'+all_renters[0].email)
    elif len(all_renters) > 1:
      return render_template('renters.html', renters=all_renters)

  return 'not found'
    