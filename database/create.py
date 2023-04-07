#from datetime import datetime
from sqlalchemy import Date, create_engine, Column, Text, Integer, ForeignKey, String, DateTime, VARCHAR, Enum, func, desc, case, select
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import case
from sqlalchemy.orm import relationship, sessionmaker, column_property

engine = create_engine('sqlite:///database.db')
engine.connect()

Base = declarative_base()


#creating the tables
'''
Data normalization
1. First normal form:
    - Each column contains only one value
    - Each row contains only one entity
    - Each table contains only one entity
    - Each table has a primary key
2. Second normal form:
    - All non-key columns are dependent on the primary key
3. Third normal form:
    - No transitive dependencies between non-key columns
4. Foruth normal form:
    - No multi-valued dependencies
'''

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
        listing_price (int): The price of the house listed for sale, in cents.
        listing_state (enum): The state of the house listing, which can be one of 'AVAILABLE', 'UNAVAILABLE', or 'SOLD'.

    Methods:
        __repr__(): A special method that returns a string representation of the Listing object. 
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(Integer, ForeignKey('houses_in_estate.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    listing_date = Column(DateTime, nullable=False)
    listing_agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    listing_office_id = Column(Integer, ForeignKey('offices.id'), nullable=False)
    listing_price = Column(Integer, nullable=False) #in cents
    listing_state = Column(
        Enum("AVAILABLE", "UNAVAILABLE", "SOLD"), default="AVAILABLE", )

    def __repr__(self):
        return "<Listing(id={0}, house_id={1}, seller_id={2}, listing_date={3}, listing_agent_id={4}, listing_office_id={5},\
            listing_price={6}, listing_state={7}>".format(
            self.id, 
            self.house_id, 
            self.seller_id, 
            self.listing_date, 
            self.listing_agent_id, 
            self.listing_office_id, 
            self.listing_price, 
            self.listing_state)


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
    __tablename__ = 'houses_in_estate'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no_of_bedrooms = Column(Integer, nullable=False)
    no_of_bathrooms = Column(Integer, nullable=False)
    address = Column(Text, nullable=False)
    zip_code = Column(Integer, nullable=False)
    office = Column(Integer, ForeignKey('offices.id'), nullable=False)
    listings = relationship("Listing", backref="house")

    def __repr__(self):
        return "<House(id={0}, no_of_bedrooms={1}, no_of_bathrooms={2}, address={3}, zip_code={4})>".format(
            self.id, 
            self.no_of_bedrooms, 
            self.no_of_bathrooms, 
            self.address, 
            self.zip_code)
    
class Agent(Base):
    '''
    The Agent class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents an agent who lists houses_in_estate for sale.

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
        return "<Agent(id={0}, firstName={1}, lastName={2}, emailAddress={3})>".format(
            self.id, 
            self.firstName, 
            self.lastName, 
            self.emailAddress)
    
class AgentOffice(Base):
    '''
    The AgentOffice class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents an agent who lists houses_in_estate for sale.

    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each agent. Primary key for the database table.
        firstName (str): The first name of the agent.
        lastName (str): The last name of the agent.

    Methods:
        __repr__(): A special method that returns a string representation of the Agent object.

    '''
    __tablename__ = "agent's office"
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    office_id = Column(Integer, ForeignKey('offices.id'))

    def __repr__(self):
        return "<AgentOffice(id={0}, agent_id={1}, office_id={2})>".format(self.id, self.agent_id,
                                                                                     self.office_id)


class Office(Base):
    '''
    The Office class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents an office where houses_in_estate are listed for sale.
    
    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each office. Primary key for the database table.
        office_name (str): The name of the office.
        listings (List[Listing]): A relationship to the Listing objects that correspond to the house that is listed for sale.

    Methods:
        __repr__(): A special method that returns a string representation of the Office object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    office_name = Column(Text)
    listings = relationship("Listing", backref="listing_office")

    def __repr__(self):
        return "<Office(id={0}, office_name={1})>".format(
            self.id, 
            self.office_name)


class Sale(Base):
    '''
    The Sale class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents a house that has been sold.
    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each house sale. Primary key for the database table.
        listing_id (int): Foreign key referencing the id of the house that was sold.
        buyer_id (int): Foreign key referencing the id of the customer who bought the house.
        sale_price (int): The price of the house that was sold, in cents.
        sell_date (datetime): The date when the house was sold.
        listing (Listing): A relationship to the Listing object that corresponds to the house that was sold.
        
    Methods:
        __repr__(): A special method that returns a string representation of the Sale object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    house_id = Column(Integer, ForeignKey('houses_in_estate.id'))
    buyer_id = Column(Integer, ForeignKey('customers.id'))
    sale_price = Column(Integer, nullable=False) #in cents
    sell_date = Column(Date, nullable=False)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    agent_commissions = column_property(
        sale_price * 
        case(
            (sale_price < 100000, 0.1),
            (sale_price < 200000, 0.075),
            (sale_price < 500000, 0.06),
            (sale_price < 1000000, 0.05),
            (sale_price >= 1000000, 0.04)
        )
    )
    listing = relationship("Listing", backref="sale", uselist=False)

    def __repr__(self):
        return "<Sale(id={0}, listing_id={1}, buyer_id={2}, sale_price={3}, sell_date={4}>".format(
            self.id, 
            self.listing_id, 
            self.buyer_id, 
            self.sale_price, 
            self.sell_date,
            self.agent_id,
            self.agent_commissions)

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
        return "<Customer(id={0}, firstName={1}, lastName={2}, emailAddress={3})>".format(
            self.id, 
            self.firstName, 
            self.lastName, 
            self.emailAddress)
    


class AgentCommission(Base):
    '''
    The AgentCommission class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents the commission that an agent receives for each sale.

    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each commission. Primary key for the database table.
        agent_id (int): Foreign key referencing the id of the agent who receives the commission.
        monthly_commission (int): The commission that the agent receives, in cents.

    Methods:
        __repr__(): A special method that returns a string representation of the AgentCommission object.
        It returns a formatted string that includes all the attributes of the object.
    '''
    __tablename__ = 'agent_commissions'
    id = Column(Integer, primary_key=True, autoincrement=True)  # unique id
    agent_id = Column(Integer, ForeignKey('agents.id'))  # id of the estate agent
    monthly_commission = Column(Integer)  # commission that the estate agent must receive

    def __repr__(self):
        return "<AgentCommission(id={0}, estate_agent_id={1}, monthly_commission={2}>".format(
            self.id,
            self.agent_id,
            self.monthly_commission)

class SalePriceSummary(Base):
    '''
    The SalePriceSummary class is an ORM (Object-Relational Mapping) model defined using SQLAlchemy.
    It represents the total sale price of all houses that have been sold.

    Attributes:
        __tablename__ (str): The name of the database table that corresponds to this model.
        id (int): A unique identifier for each sale price summary. Primary key for the database table.
        total_sale (int): The total sale price of all houses that have been sold, in cents.

    Methods:
        __repr__(): A special method that returns a string representation of the SalePriceSummary object.
        It returns a formatted string that includes all the attributes of the object.
    '''

    __tablename__ = 'summ_sale_prices'
    id = Column(Integer, primary_key=True, autoincrement=True)  # unique id
    total_sale = Column(Integer)  # the sum of all sale prices

    def __repr__(self):
        return "<SalePriceSummary(id={0}, total_sale={1}>".format(
            self.id,
            self.total_sale)



Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

#schema for all tables created
#print(Base.metadata.tables)
print(repr(Customer))
print(repr(Listing))
print(repr(Sale))
print(repr(Agent))
print(repr(House))
print(repr(Office))
print(repr(AgentCommission))
print(repr(SalePriceSummary))
print(repr(AgentOffice))