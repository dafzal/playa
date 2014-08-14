from bike import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
import re

class Renter(Base):
  __tablename__ = 'renter'
  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=False)
  email = Column(String(255), unique=False)
  code = Column(String(255), unique=True)
  bikes = relationship('Bike', backref=backref('renter'))
  zipcode = Column(String(255))
  phone = Column(String(255))
  desc = Column(String)
  qty = Column(Integer)

  def __init__(self, name=None, email=None, 
    code=None, qty=None, desc=None, zipcode=None, phone=None):
    self.name = name
    self.email = email
    self.code = code
    self.qty = qty
    self.desc = desc
    self.zipcode = zipcode
    self.phone = re.sub('[^\d]','',phone or '')

  def __repr__(self):
    return 'Renter %r %r' % (self.name, self.code)

  def attach_bike(self, bike):
    if 'bike rental' not in self.desc.lower():
      return False, 'Not valid rental ' + self.desc
    if len(self.bikes) >= self.qty:
      return False, 'Too many bikes rented:%d reservation:%d' % (len(self.bikes), self.qty)
    self.bikes.append(bike)
    return True, ''

class Bike(Base):
  __tablename__ = 'bike'
  id = Column(Integer, primary_key=True)
  renter_id = Column(Integer, ForeignKey('renter.id'))
  code = Column(String(255), unique=True)
  comment = Column(String)

  def __init__(self, code=None):
    self.code = code  
  def __repr__(self):
    return 'Bike %r' % (self.code)