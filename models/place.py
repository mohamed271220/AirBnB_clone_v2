#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import (Column, String,
                        ForeignKey, Float,
                        Integer, Table)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage
from models.amenity import Amenity

association_table = Table('place_amenities', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary="place_amenities", viewonly=False, cascade="all, delete-orphan", overlaps="place_amenities")
    
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """getter attribute reviews that returns the list of Review instances"""
            from models import storage
            from models.review import Review
            review_list = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list
        
        @property
        def amenities(self):
            """
            getter attribute amenities that returns the list of Amenity instances
            """
            amenity_list = []
            for amenity in storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list
        
        @amenities.setter
        def amenities(self, obj):
            """
            setter attribute amenities that handles append method for adding an Amenity.id
            to the attribute amenity_ids
            """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
                