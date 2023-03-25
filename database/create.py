from datetime import datetime
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, String, DateTime, VARCHAR, Enum, func, desc, case, select
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///database.db')
engine.connect()

Base = sqlalchemy.orm.declarative_base()

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    seller_id = Column(Integer, ForeignKey('customers.id'))
    listing_date = Column(DateTime, nullable=False, default=datetime.now)
    listing_agent_id = Column(Integer, ForeignKey('agents.id'))
    listing_office_id = Column(Integer, ForeignKey('offices.id'))
    listing_price_IN_CENTS = Column(Integer, nullable=False)
    listing_state = Column(
        Enum("AVAILABLE", "UNAVAILABLE", "SOLD"), default="AVAILABLE")

    def __repr__(self):
        return "<Listing(id={0}, house_id={1}, seller_id={2}, listing_date={3}, listing_agent_id={4}, listing_office_id={5},\
            listing_price_IN_CENTS={6}, listing_state={7}>".format(self.id, self.house_id, self.seller_id, self.listing_date, self.listing_agent_id, self.listing_office_id, self.listing_price_IN_CENTS, self.listing_state)


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    buyer_id = Column(Integer, ForeignKey('customers.id'))
    sell_price_IN_CENTS = Column(Integer, nullable=False)
    sell_date = Column(DateTime, nullable=False, default=datetime.now)
    listing = relationship("Listing", backref="sale", uselist=False)

    def __repr__(self):
        return "<Sale(id={0}, listing_id={1}, buyer_id={2}, sell_price_IN_CENTS={3}, sell_date={4}>".format(self.id, self.listing_id, self.buyer_id, self.sell_price_IN_CENTS, self.sell_date)


class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    no_of_bedrooms = Column(Integer, nullable=False)
    no_of_bathrooms = Column(Integer, nullable=False)
    address = Column(Text, nullable=False)
    zip_code = Column(String(5), nullable=False)
    listings = relationship("Listing", backref="house")

    def __repr__(self):
        return "<House(id={0}, no_of_bedrooms={1}, no_of_bathrooms={2}, address={3}, zip_code={4})>".format(self.id, self.no_of_bedrooms, self.no_of_bathrooms, self.address, self.zip_code)


class Office(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    location = Column(Text, nullable=False, unique=True)
    listings = relationship("Listing", backref="listing_office")

    def __repr__(self):
        return "<Office(id={0}, location={1})>".format(self.id, self.location)


class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    firstName = Column(Text, nullable=False)
    lastName = Column(Text, nullable=False)
    emailAddress = Column(VARCHAR(40), nullable=False, unique=True)
    listings = relationship("Listing", backref="listing_agent")

    def __repr__(self):
        return "<Agent(id={0}, firstName={1}, lastName={2}, emailAddress={3})>".format(self.id, self.firstName, self.lastName, self.emailAddress)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    firstName = Column(Text, nullable=False)
    lastName = Column(Text, nullable=False)
    emailAddress = Column(VARCHAR(40), nullable=False, unique=True)
    buy_invoices = relationship("Sale", backref="buyer")
    listings = relationship("Listing", backref="seller")

    def __repr__(self):
        return "<Customer(id={0}, firstName={1}, lastName={2}, emailAddress={3})>".format(self.id, self.firstName, self.lastName, self.emailAddress)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
