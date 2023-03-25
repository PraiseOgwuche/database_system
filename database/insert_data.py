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
    """
    Check first if there is a referenced listing, buyer, and office for this proposed listing and if not rollback.
    If there is, proceed to add new listing to the database. 
    At that step, we check if the proposed listing is still available as that may change if the owner has sold the house through another listing.

    Args:
        buyer_id (integer): The buyer id that represents the person hoping to buy the listing.
        listing_id (integer): The listing id that represents the listing being suggested for a sale
        sell_price_in_cents (integer): The bid price proposed by the buyer and accepted by the seller.
        sell_date (_type_, optional): The date that the proposed listing was sold. Defaults to None.
    """
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
    except:
        session.rollback()


def register_new_house(no_of_bedrooms, no_of_bathrooms, address, zip_code):
    """
    Check first if there is an house that is already covered by the proposed address and rollback if already present.
    If not, proceed to add new house to the database.

    Args:
        no_of_bedrooms (integer): The number of bedrooms in the house to be registered
        no_of_bathrooms (integer): The number of bathrooms in the house to be registered
        address (text): The address of the house to be registered
        zip_code (integer): The zip code representing the locaiton of the house to be registered
    """
    session = Session()
    session.begin()
    if no_of_bedrooms is None or no_of_bathrooms is None or address is None or zip_code is None:
        print("None of the parameters should be None")
        session.rollback()
        return
    house = session.query(House).filter(House.address == address).first()
    if house:
        print("A house has already been registered for that address")
        session.rollback()
        return
    try:
        new_house = House(no_of_bedrooms=no_of_bedrooms, no_of_bathrooms=no_of_bathrooms,
                          address=address, zip_code=zip_code)
        session.add(new_house)
        session.commit()
        print(new_house)
    except:
        session.rollback()


def register_new_listing(house_id, seller_id, listing_agent_id, listing_office_id, listing_price_in_cents, listing_date=None):
    """
    Check first if there is a referenced house, seller, agent, and office for this proposed listing and if not rollback.
    If there is, proceed to add new listing to the database.

    Args:
        house_id (integer): The house id that represents the home being sold.
        seller_id (integer): The seller id that represents the owner hoping to sell their house.
        listing_agent_id (integer): The agent id that represents the agent hosting the proposed listing.
        listing_office_id (integer): The office id that represents the office hosting the proposed listing.
        listing_price_in_cents (integer): The asking price for this listing as requested by the seller.
    """
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
    except:
        session.rollback()


def register_new_office(location):
    """
    Check first if there is an office location that is already covered by the proposed location and rollback if already present.
    If not, proceed to add new office location to the database.

    Args:
        location (string): location coverage for that particular office
    """
    session = Session()
    session.begin()
    office = session.query(Office).filter(
        Office.location == location).first()
    if office:
        print("An office has already been registered under that location")
        session.rollback()
        return
    try:
        new_office = Office(location=location)
        session.add(new_office)
        session.commit()
        print(new_office)
    except:
        session.rollback()


def register_new_agent(firstName, lastName, emailAddress):
    """
    Check first if there is a agent that exists in the database with said email address and rollback if already present.
    If not, proceed to add new agent to the database.

    Args:
        firstName (string): first name of the new agent
        lastName (string): last name of the new agent
        emailAddress (string): email address to contact the new agent
    """
    session = Session()
    session.begin()
    agent = session.query(Agent).filter(
        Agent.emailAddress == emailAddress).first()
    if agent:
        print("An agent has already been registered under that name")
        session.rollback()
        return
    try:
        new_agent = Agent(firstName=firstName, lastName=lastName,
                          emailAddress=emailAddress)
        session.add(new_agent)
        session.commit()
        print(new_agent)
    except:
        session.rollback()


def register_new_customer(firstName, lastName, emailAddress):
    """
    Check first if there is a customer that exists in the database with said email address and rollback if already present.
    If not, proceed to add new customer to the database.

    Args:
        firstName (string): first name of the new customer
        lastName (string): last name of the new customer
        emailAddress (string): email address to contact the new customer
    """
    session = Session()
    session.begin()
    customer = session.query(Customer).filter(
        Customer.emailAddress == emailAddress).first()
    if customer:
        print("A customer has already been registered under that email address")
        session.rollback()
        return
    try:
        new_customer = Customer(firstName=firstName, lastName=lastName,
                                emailAddress=emailAddress)
        session.add(new_customer)
        session.commit()
        print(new_customer)
    except:
        session.rollback()


def query_data():

    session = Session()

    print('"""')
    print('Find the top 5 offices with the most sales for that month.')
    print('"""')
    print(session.query(Office.location, func.count(Listing.house_id).label("homes_sold")).join(Listing, Office.id == Listing.listing_office_id).join(Sale, Listing.id == Sale.listing_id).filter(
        Listing.listing_state == 'SOLD', extract('month', Sale.sell_date) == datetime.now().month).group_by(Office.id).order_by(desc("homes_sold")).limit(5).all())

    print('"""')
    print('Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).')
    print('"""')
    print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
        Sale, Sale.listing_id == Listing.id).filter(extract('month', Sale.sell_date) == datetime.now().month).group_by(Agent.id).order_by(desc(func.sum(Sale.sell_price_IN_CENTS))).all())

    print('"""')
    print('Calculate the commission that each estate agent must receive and store the results in a separate table.')
    print('"""')
    stmt = session.query(Agent, func.sum(
        case((Sale.sell_price_IN_CENTS is None, 0),
             (Sale.sell_price_IN_CENTS <= 10000000, 0.1*Sale.sell_price_IN_CENTS),
             (and_(10000000 < Sale.sell_price_IN_CENTS, Sale.sell_price_IN_CENTS <=
                   20000000), 0.075*Sale.sell_price_IN_CENTS),
             (and_(20000000 < Sale.sell_price_IN_CENTS, Sale.sell_price_IN_CENTS <=
                   50000000), 0.06*Sale.sell_price_IN_CENTS),
             (and_(50000000 < Sale.sell_price_IN_CENTS, Sale.sell_price_IN_CENTS <=
                   100000000), 0.05*Sale.sell_price_IN_CENTS),
             else_=0.04*Sale.sell_price_IN_CENTS))).outerjoin(Listing, Listing.listing_agent_id == Agent.id).outerjoin(Sale, Sale.listing_id == Listing.id).filter(extract('month', Sale.sell_date) == datetime.now().month).group_by(Agent.id)

    case((Sale.sell_price_IN_CENTS is None, 0),
         (Sale.sell_price_IN_CENTS <= 10000000, 0.1*Sale.sell_price_IN_CENTS),
         (Sale.sell_price_IN_CENTS <= 10000000, 0.1*Sale.sell_price_IN_CENTS))
    print(stmt.all())

    print('"""')
    print('For all houses that were sold that month, calculate the average number of days on the market.')
    print('"""')
    print(session.query(func.avg(cast(func.julianday(Sale.sell_date) - func.julianday(Listing.listing_date), Integer)))
          .join(Listing, Listing.id == Sale.listing_id).filter(extract('month', Sale.sell_date) == datetime.now().month).first()[0])

    print('"""')
    print('For all houses that were sold that month, calculate the average selling price.')
    print('"""')
    print(session.execute(select(func.avg(Sale.sell_price_IN_CENTS)).filter(
        extract('month', Sale.sell_date) == datetime.now().month)).first()[0])


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
