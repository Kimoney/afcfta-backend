# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Define naming convention
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)


class Country(db.Model, SerializerMixin):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    
    # Relationships
    indicator_values = db.relationship('IndicatorValue', back_populates='country')


class Year(db.Model, SerializerMixin):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)

    # Relationships
    indicator_values = db.relationship('IndicatorValue', back_populates='year')


class Indicator(db.Model, SerializerMixin):
    __tablename__ = 'indicators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    # Relationships
    indicator_values = db.relationship('IndicatorValue', back_populates='indicator')


class IndicatorValue(db.Model, SerializerMixin):
    __tablename__ = 'indicator_values'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=True)
    
    # Foreign keys
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=False)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'), nullable=False)
    
    # Relationships
    country = db.relationship('Country', back_populates='indicator_values')
    year = db.relationship('Year', back_populates='indicator_values')
    indicator = db.relationship('Indicator', back_populates='indicator_values')
