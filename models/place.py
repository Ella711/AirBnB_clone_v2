#!/usr/bin/python3
""" Place Module for HBNB project """
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.review import Review
from os import getenv
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            'Review', backref='place', cascade='all, delete')

        place_amenity = Table(
            'place_amenity', Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   primary_key=True, nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   primary_key=True, nullable=False)
        )

        amenities = relationship(
            'Amenity', secondary=place_amenity, viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """ Return the list of Reviews by Place """
            from models import storage
            reviews_by_place = []
            for rev in storage.all(Review).values():
                if rev.place_id == self.id:
                    reviews_by_place.append(rev)
            return reviews_by_place

        @property
        def amenities(self):
            """ Return the list of Amenities by Place """
            from models import storage
            amenities_by_place = []
            for amen in storage.all(Amenity).values():
                if amen.place_id == self.id:
                    amenities_by_place.append(amen)
            return amenities_by_place

        @amenities.setter
        def amenities(self, obj):
            """ Adds an Amenity.id to the attribute amenity_ids """
            if obj.__class__.__name__ == 'Amenity':
                self.amenity_ids.append(obj)
