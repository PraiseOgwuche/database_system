from datetime import datetime
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, String, DateTime, VARCHAR, Enum, func, desc, case, select
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///database.db')
engine.connect()

Base = sqlalchemy.orm.declarative_base()

class Listing(Base):
    '''
    The Listing class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy. 
    It represents a house that is listed for sale. 

    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each house listing. Primary key for the database table.
        house_id (int): Foreign key referencing the id of the house that is being listed for sale.
        seller_id (int): Foreign key referencing the id of the customer who is selling the house.
        listing_date (datetime): The date when the house was listed for sale.
        listing_agent_id (int): Foreign key referencing the id of the agent who listed the house for sale.
        listing_office_id (int): Foreign key referencing the id of the office where the house is listed for sale.
        listing_price_IN_CENTS (int): The price of the house listed for sale, in cents.
        listing_state (enum): The state of the house listing, which can be one of 'AVAILABLE', 'UNAVAILABLE', or 'SOLD'.

    Methods:
        __repr__(): A special method that returns a string representation of the Listing object. 
        It returns a formatted string that includes all the attributes of the object.
    '''
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


class House(Base):
    '''
    The House class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents a house that is listed for sale.

    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each house. Primary key for the database table.
        no_of_bedrooms (int): The number of bedrooms in the house.
        no_of_bathrooms (int): The number of bathrooms in the house.
        address (str): The address of the house.
        zip_code (str): The zip code of the house.
        listings (List[Listing]): A relationship to the Listing objects that correspond to the house that is listed for sale.

    Methods:
        __repr__(): A special method that returns a string representation of the House object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    no_of_bedrooms = Column(Integer, nullable=False)
    no_of_bathrooms = Column(Integer, nullable=False)
    address = Column(Text, nullable=False)
    zip_code = Column(String(5), nullable=False)
    listings = relationship("Listing", backref="house")

    def __repr__(self):
        return "<House(id={0}, no_of_bedrooms={1}, no_of_bathrooms={2}, address={3}, zip_code={4})>".format(self.id, self.no_of_bedrooms, self.no_of_bathrooms, self.address, self.zip_code)


class Sale(Base):
    '''
    The Sale class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents a house that has been sold.
    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each house sale. Primary key for the database table.
        listing_id (int): Foreign key referencing the id of the house that was sold.
        buyer_id (int): Foreign key referencing the id of the customer who bought the house.
        sell_price_IN_CENTS (int): The price of the house that was sold, in cents.
        sell_date (datetime): The date when the house was sold.
        listing (Listing): A relationship to the Listing object that corresponds to the house that was sold.
        
    Methods:
        __repr__(): A special method that returns a string representation of the Sale object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    buyer_id = Column(Integer, ForeignKey('customers.id'))
    sell_price_IN_CENTS = Column(Integer, nullable=False)
    sell_date = Column(DateTime, nullable=False, default=datetime.now)
    listing = relationship("Listing", backref="sale", uselist=False)

    def __repr__(self):
        return "<Sale(id={0}, listing_id={1}, buyer_id={2}, sell_price_IN_CENTS={3}, sell_date={4}>".format(self.id, self.listing_id, self.buyer_id, self.sell_price_IN_CENTS, self.sell_date)


class Agent(Base):
    '''
    The Agent class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents an agent who lists houses for sale.

    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each agent. Primary key for the database table.
        firstName (str): The first name of the agent.
        lastName (str): The last name of the agent.
        emailAddress (str): The email address of the agent.
        listings (List[Listing]): A relationship to the Listing objects that correspond to the house that is listed for sale.

    Methods:
        __repr__(): A special method that returns a string representation of the Agent object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    firstName = Column(Text, nullable=False)
    lastName = Column(Text, nullable=False)
    emailAddress = Column(VARCHAR(40), nullable=False, unique=True)
    listings = relationship("Listing", backref="listing_agent")

    def __repr__(self):
        return "<Agent(id={0}, firstName={1}, lastName={2}, emailAddress={3})>".format(self.id, self.firstName, self.lastName, self.emailAddress)


class Customer(Base):
    '''
    The Customer class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents a customer who buys a house.

    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each customer. Primary key for the database table.
        firstName (str): The first name of the customer.
        lastName (str): The last name of the customer.
        emailAddress (str): The email address of the customer.
        buy_invoices (List[Sale]): A relationship to the Sale objects that correspond to the house that was sold.
        listings (List[Listing]): A relationship to the Listing objects that correspond to the house that is listed for sale.

    Methods:
        __repr__(): A special method that returns a string representation of the Customer object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    firstName = Column(Text, nullable=False)
    lastName = Column(Text, nullable=False)
    emailAddress = Column(VARCHAR(40), nullable=False, unique=True)
    buy_invoices = relationship("Sale", backref="buyer")
    listings = relationship("Listing", backref="seller")

    def __repr__(self):
        return "<Customer(id={0}, firstName={1}, lastName={2}, emailAddress={3})>".format(self.id, self.firstName, self.lastName, self.emailAddress)
    

class Office(Base):
    '''
    The Office class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents an office where houses are listed for sale.
    
    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each office. Primary key for the database table.
        location (str): The location of the office.
        listings (List[Listing]): A relationship to the Listing objects that correspond to the house that is listed for sale.

    Methods:
        __repr__(): A special method that returns a string representation of the Office object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    location = Column(Text, nullable=False, unique=True)
    listings = relationship("Listing", backref="listing_office")

    def __repr__(self):
        return "<Office(id={0}, location={1})>".format(self.id, self.location)



Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

