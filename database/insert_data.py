from sqlalchemy import create_engine
from sqlalchemy.sql import extract, select
from sqlalchemy.orm import relationship, sessionmaker
from create import House, Listing, Office, Agent, Customer, Sale
from faker import Faker
from datetime import datetime
from sqlalchemy import create_engine, func, desc, case, cast, Integer, and_


engine = create_engine('sqlite:///database.db')
engine.connect()

Session = sessionmaker(bind=engine)


def register_new_sale(buyer_id, listing_id, sell_price_in_cents, sell_date=None):
    '''
    Check first if the buyer is registered and the listing is available.
    If not, rollback the transaction.
    If yes, proceed to add new sale to the database.
    
    Args:
        buyer_id (integer): The id of the buyer
        listing_id (integer): The id of the listing
        sell_price_in_cents (integer): The price of the sale in cents
        sell_date (datetime): The date of the sale

    Returns:
        None
    '''
    session = Session()
    session.begin()
    if buyer_id is None or listing_id is None or sell_price_in_cents is None:
        print("None of the parameters should be None")
        session.rollback()
        return
    buyer = session.get(Customer, buyer_id)
    if buyer is None:
        print("Please register the customer first")
        session.rollback()
        return
    listing = session.query(Listing).filter(
        Listing.id == listing_id, Listing.listing_state == "AVAILABLE").first()
    if listing is None:
        print("There is no such listing registered and still available")
        session.rollback()
        return
    session.query(Listing).filter(
        Listing.listing_state == "AVAILABLE", Listing.id != listing.id, Listing.house_id == listing.house_id).update({Listing.listing_state: "UNAVAILABLE"})
    # update(Listing).values(listing_state="UNAVAILABLE").where(
    #     Listing.house_id == listing.house.id)
    listing.listing_state = "SOLD"
    if sell_date:
        new_sale = Sale(sell_price_IN_CENTS=sell_price_in_cents,
                        sell_date=sell_date)
    else:
        new_sale = Sale(sell_price_IN_CENTS=sell_price_in_cents)
    try:
        new_sale.listing = listing
        new_sale.buyer = buyer
        session.add(new_sale)
        session.commit()
        print(new_sale)
    except Exception:
        session.rollback()


def register_new_house(no_of_bedrooms, no_of_bathrooms, address, zip_code):
    '''
    Check first if there is a house registered for the given address.
    If yes, rollback the transaction.
    If no, proceed to add new house to the database.
    
    Args:
        no_of_bedrooms (integer): The number of bedrooms in the house
        no_of_bathrooms (integer): The number of bathrooms in the house
        address (string): The address of the house
        zip_code (integer): The zip code of the house
        
    Returns:
        None
    '''
    session = Session()
    session.begin()
    if no_of_bedrooms is None or no_of_bathrooms is None or address is None or zip_code is None:
        print("None of the parameters should be None")
        session.rollback()
        return
    if house := session.query(House).filter(House.address == address).first():
        print("A house has already been registered for that address")
        session.rollback()
        return
    try:
        new_house = House(no_of_bedrooms=no_of_bedrooms, no_of_bathrooms=no_of_bathrooms,
                          address=address, zip_code=zip_code)
        session.add(new_house)
        session.commit()
        print(new_house)
    except Exception:
        session.rollback()


def register_new_listing(house_id, seller_id, listing_agent_id, listing_office_id, listing_price_in_cents, listing_date=None):
    '''
    Check first if the house, seller, listing agent and listing office are registered.
    If not, rollback the transaction.
    If yes, proceed to add new listing to the database.
    
    Args:
        house_id (integer): The id of the house
        seller_id (integer): The id of the seller
        listing_agent_id (integer): The id of the listing agent
        listing_office_id (integer): The id of the listing office
        listing_price_in_cents (integer): The price of the listing in cents
        listing_date (datetime): The date of the listing
        
    Returns:
        None
    '''
    session = Session()
    session.begin()
    if house_id is None or seller_id is None or listing_agent_id is None or listing_office_id is None or listing_price_in_cents is None:
        print("None of the parameters should be None")
        session.rollback()
        return
    house = session.get(House, house_id)
    if house is None:
        print("There is no such house registered")
        session.rollback()
        return
    seller = session.get(Customer, seller_id)
    if seller is None:
        print("Please register the customer first")
        session.rollback()
        return
    listing_agent = session.get(Agent, listing_agent_id)
    if listing_agent is None:
        print("There is no such agent registered")
        session.rollback()
        return
    listing_office = session.get(Office, listing_office_id)
    if listing_office is None:
        print("There is no such office registered")
        session.rollback()
        return
    try:
        if listing_date:
            new_listing = Listing(
                listing_price_IN_CENTS=listing_price_in_cents, listing_date=listing_date)
        else:
            new_listing = Listing(
                listing_price_IN_CENTS=listing_price_in_cents)
        new_listing.seller = seller
        new_listing.house = house
        new_listing.listing_agent = listing_agent
        new_listing.listing_office = listing_office
        session.add(new_listing)
        session.commit()
        print(new_listing)
    except Exception:
        session.rollback()


def register_new_office(location):
    '''
    Check first if there is an office registered for the given location.
    If yes, rollback the transaction.
    If no, proceed to add new office to the database.
    
    Args:
        location (string): The location of the office
        
    Returns:
        None
    '''
    session = Session()
    session.begin()
    if (
        office := session.query(Office)
        .filter(Office.location == location)
        .first()
    ):
        print("An office has already been registered under that location")
        session.rollback()
        return
    try:
        new_office = Office(location=location)
        session.add(new_office)
        session.commit()
        print(new_office)
    except Exception:
        session.rollback()


def register_new_agent(firstName, lastName, emailAddress):
    '''
    Check first if there is an agent registered for the given email address.
    If yes, rollback the transaction.
    If no, proceed to add new agent to the database.
    
    Args:
        firstName (string): The first name of the agent
        lastName (string): The last name of the agent
        emailAddress (string): The email address of the agent
        
    Returns:
        None
    '''
    session = Session()
    session.begin()
    if (
        agent := session.query(Agent)
        .filter(Agent.emailAddress == emailAddress)
        .first()
    ):
        print("An agent has already been registered under that name")
        session.rollback()
        return
    try:
        new_agent = Agent(firstName=firstName, lastName=lastName,
                          emailAddress=emailAddress)
        session.add(new_agent)
        session.commit()
        print(new_agent)
    except Exception:
        session.rollback()


def register_new_customer(firstName, lastName, emailAddress):
    '''
    Check first if there is a customer registered for the given email address.
    If yes, rollback the transaction.
    If no, proceed to add new customer to the database.
    
    Args:
        firstName (string): The first name of the customer
        lastName (string): The last name of the customer
        emailAddress (string): The email address of the customer
        
    Returns:
        None
    '''
    session = Session()
    session.begin()
    if (
        customer := session.query(Customer)
        .filter(Customer.emailAddress == emailAddress)
        .first()
    ):
        print("A customer has already been registered under that email address")
        session.rollback()
        return
    try:
        new_customer = Customer(firstName=firstName, lastName=lastName,
                                emailAddress=emailAddress)
        session.add(new_customer)
        session.commit()
        print(new_customer)
    except Exception:
        session.rollback()


def query_data():
    '''
    Query the database for the following information:
    1. Find the top 5 houses with the highest price.
    2. Find the top 5 houses with the lowest price.
    3. Find the top 5 houses with the highest price per square foot.
    4. Find the top 5 houses with the lowest price per square foot.
    5. Find the top 5 offices with the most sales for that month.
    6. Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
    7. Find the top 5 estate agents who have sold the least for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
    8. Find the top 5 estate agents who have sold the most for the year (include their contact details and their sales details so that it is easy contact them and congratulate them).
    9. Find the top 5 estate agents who have sold the least for the year (include their contact details and their sales details so that it is easy contact them and congratulate them).
    '''

    session = Session()

    _extracted_from_query_data_5(
        'Find the top 5 offices with the most sales for that month.'
    )
    print(session.query(Office.location, func.count(Listing.house_id).label("homes_sold")).join(Listing, Office.id == Listing.listing_office_id).join(Sale, Listing.id == Sale.listing_id).filter(
        Listing.listing_state == 'SOLD', extract('month', Sale.sell_date) == datetime.now().month).group_by(Office.id).order_by(desc("homes_sold")).limit(5).all())

    _extracted_from_query_data_5(
        'Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).'
    )
    print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
        Sale, Sale.listing_id == Listing.id).filter(extract('month', Sale.sell_date) == datetime.now().month).group_by(Agent.id).order_by(desc(func.sum(Sale.sell_price_IN_CENTS))).all())

    _extracted_from_query_data_5(
        'Find the top 5 estate agents who have sold the least for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).'
    )
    print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
        Sale, Sale.listing_id == Listing.id).filter(extract('month', Sale.sell_date) == datetime.now().month).group_by(Agent.id).order_by(func.sum(Sale.sell_price_IN_CENTS)).all())
    
    _extracted_from_query_data_5(
        'Find the top 5 estate agents who have sold the most for the year (include their contact details and their sales details so that it is easy contact them and congratulate them).'
    )
    print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
        Sale, Sale.listing_id == Listing.id).filter(extract('year', Sale.sell_date) == datetime.now().year).group_by(Agent.id).order_by(desc(func.sum(Sale.sell_price_IN_CENTS))).all())
    
    _extracted_from_query_data_5(
        'Find the top 5 estate agents who have sold the least for the year (include their contact details and their sales details so that it is easy contact them and congratulate them).'
    )
    print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
        Sale, Sale.listing_id == Listing.id).filter(extract('year', Sale.sell_date) == datetime.now().year).group_by(Agent.id).order_by(func.sum(Sale.sell_price_IN_CENTS)).all())

    _extracted_from_query_data_5(
        'Calculate the commission that each estate agent must receive and store the results in a separate table.'

    )
    stmt = (
        session.query(
            Agent,
            func.sum(
                case(
                    (Sale.sell_price_IN_CENTS is None, 0),
                    (
                        Sale.sell_price_IN_CENTS <= 10000000,
                        0.1 * Sale.sell_price_IN_CENTS,
                    ),
                    (
                        and_(
                            Sale.sell_price_IN_CENTS > 10000000,
                            Sale.sell_price_IN_CENTS <= 20000000,
                        ),
                        0.075 * Sale.sell_price_IN_CENTS,
                    ),
                    (
                        and_(
                            Sale.sell_price_IN_CENTS > 20000000,
                            Sale.sell_price_IN_CENTS <= 50000000,
                        ),
                        0.06 * Sale.sell_price_IN_CENTS,
                    ),
                    (
                        and_(
                            Sale.sell_price_IN_CENTS > 50000000,
                            Sale.sell_price_IN_CENTS <= 100000000,
                        ),
                        0.05 * Sale.sell_price_IN_CENTS,
                    ),
                    else_=0.04 * Sale.sell_price_IN_CENTS,
                )
            ),
        )
        .outerjoin(Listing, Listing.listing_agent_id == Agent.id)
        .outerjoin(Sale, Sale.listing_id == Listing.id)
        .filter(extract('month', Sale.sell_date) == datetime.now().month)
        .group_by(Agent.id)
    )

    case((Sale.sell_price_IN_CENTS is None, 0),
         (Sale.sell_price_IN_CENTS <= 10000000, 0.1*Sale.sell_price_IN_CENTS),
         (Sale.sell_price_IN_CENTS <= 10000000, 0.1*Sale.sell_price_IN_CENTS))
    print(stmt.all())

    _extracted_from_query_data_5(
        'For all houses that were sold that month, calculate the average number of days on the market.'
    )
    print(session.query(func.avg(cast(func.julianday(Sale.sell_date) - func.julianday(Listing.listing_date), Integer)))
          .join(Listing, Listing.id == Sale.listing_id).filter(extract('month', Sale.sell_date) == datetime.now().month).first()[0])

    _extracted_from_query_data_5(
        'For all houses that were sold that month, calculate the average selling price.'
    )
    print(session.execute(select(func.avg(Sale.sell_price_IN_CENTS)).filter(
        extract('month', Sale.sell_date) == datetime.now().month)).first()[0])


# TODO Rename this here and in `query_data`
def _extracted_from_query_data_5(arg0):
    print('"""')
    print(arg0)
    print('"""')


if __name__ == "__main__":
    """
    Generate Fake data for testing
    """
    fake = Faker()
    for _ in range(20):
        register_new_customer(
            fake.first_name(), fake.last_name(), fake.unique.email())
        register_new_agent(fake.first_name(),
                           fake.last_name(), fake.unique.email())
    for _ in range(20):
        register_new_office(fake.address())
        register_new_house(fake.random_int(min=1, max=30), fake.random_int(min=1, max=30),
                           fake.street_address(), fake.postcode())

    for _ in range(20):
        register_new_listing(fake.random_int(min=1, max=20), fake.random_int(min=1, max=20), fake.random_int(min=1, max=20),
                             fake.random_int(min=1, max=20), fake.random_int(min=5000000, max=3000000000), listing_date=fake.date_time_this_year())

    for _ in range(20):
        register_new_sale(fake.random_int(min=1, max=20),
                          fake.random_int(min=1, max=20), fake.random_int(min=5000000, max=3000000000))

    query_data()
