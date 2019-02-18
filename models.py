import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import random
import string
import httplib2

Base = declarative_base()

secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in xrange(32))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    email = Column(String, index=True)


class HelperMixin(object):
    @classmethod
    def verify_valid_pic(cls, url):
        h = httplib2.Http()
        try:
            response_header = h.request(url, 'GET')[0]
            ping_status_code = response_header['status']
            content_type = response_header['content-type']
            if ping_status_code != "200" or 'image' not in content_type:
                # If the resource doesn't exist or isn't image, don't save it
                result = None
            else:
                result = url
        except:
            result = None
        return result

    def validate_object(self):
        if self.name == '':
            return False
        else:
            return True


class Food(HelperMixin, Base):
    __tablename__ = 'food'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250))
    protected = Column(Boolean, default=False)

    @property
    def serialize(self):

        return {
           'name': self.name,
           'id': self.id,
        }

var_char_table = Table('association', Base.metadata,
                       Column('variety_id', Integer, ForeignKey('variety.id')),
                       Column('characteristic_id', Integer,
                              ForeignKey('characteristic.id')),
                       )


class Variety(HelperMixin, Base):
    __tablename__ = 'variety'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    food_id = Column(Integer, ForeignKey('food.id'))
    food = relationship(Food)
    picture = Column(String(250))
    characteristics = relationship('Characteristic',
                                   secondary=var_char_table)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        variety_hash = {
                        'name': self.name,
                        'description': self.description,
                        'id': self.id,
                        'food': self.food.name,
                       }
        variety_hash['characteristics'] = []
        for c in self.characteristics:
            variety_hash['characteristics'].append(c.char)
        return variety_hash


class Characteristic(Base):
    __tablename__ = 'characteristic'

    char = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///FoodVarieties.db')

Base.metadata.create_all(engine)
