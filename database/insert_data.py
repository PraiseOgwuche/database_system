from sqlalchemy import create_engine, insert
from sqlalchemy.sql import extract, select
from sqlalchemy.orm import relationship, sessionmaker
from create import House, Listing, Office, Agent, Customer, Sale, AgentCommission, AgentOffice, SalePriceSummary, Base, engine
from faker import Faker
from datetime import datetime
from sqlalchemy import create_engine, func, desc, case, cast, Integer, and_


Session = sessionmaker(bind=engine)
session = Session()

session.add(Customer(firstName='Praise', lastName='Ogwuche', emailAddress='praiseogwuche@staple.com'))
session.add(Customer(firstName='Jane', lastName='Doe', emailAddress='jane.doe@example.com'))
session.add(Customer(firstName='Michael', lastName='Smith', emailAddress='michael.smith@example.com'))
session.add(Customer(firstName='Emma', lastName='Johnson', emailAddress='emma.johnson@cred.edu'))
session.add(Customer(firstName='Olivia', lastName='Williams', emailAddress='olivia1@greenshaw.com'))

session.add(Office(office_name= 'south san francisco'))
session.add(Office(office_name= 'san francisco'))
session.add(Office(office_name= 'san jose'))
session.add(Office(office_name= 'oakland'))
session.add(Office(office_name= 'santa clara'))
session.add(Office(office_name= 'sunnyvale'))
session.add(Office(office_name= 'san mateo'))
session.add(Office(office_name= 'berkeley'))

session.add(Agent(firstName='Wagwan', lastName='Shaw', emailAddress='wawanshaw@realtor.com'))
session.add(Agent(firstName='Stella', lastName='Knowles', emailAddress='stella@realtor.com'))
session.add(Agent(firstName='Blessing', lastName='Stay', emailAddress='blessing@realtor.com'))
session.add(Agent(firstName='Fie', lastName='Fie', emailAddress='fie@realtor.com'))
session.add(Agent(firstName='Ben', lastName='Foe', emailAddress='foe@finestreally.co')) 
session.add(Agent(firstName='Destiny', lastName='Freeman', emailAddress='freeman@finestreally.co'))

session.add(AgentOffice(office_id=1, agent_id=1))
session.add(AgentOffice(office_id=2, agent_id=2))
session.add(AgentOffice(office_id=3, agent_id=3))
session.add(AgentOffice(office_id=1, agent_id=4))
session.add(AgentOffice(office_id=5, agent_id=1))
session.add(AgentOffice(office_id=1, agent_id=1))
session.add(AgentOffice(office_id=6, agent_id=1))
session.add(AgentOffice(office_id=8, agent_id=4))
session.add(AgentOffice(office_id=4, agent_id=3))
    

session.add(House(no_of_bedrooms=3, no_of_bathrooms=3, address='1233 Market Street, San Francisco, CA', zip_code=94111, office = 3))
session.add(House(no_of_bedrooms=4, no_of_bathrooms=3, address='13 Fell Street, San Francisco, CA', zip_code=94110, office = 3))
session.add(House(no_of_bedrooms=2, no_of_bathrooms=2, address='16 Turk Street, San Jose, CA', zip_code=94102, office = 4))
session.add(House(no_of_bedrooms=3, no_of_bathrooms=2, address='1248 Market Street, Berkeley, CA', zip_code=12345, office = 2))
session.add(House(no_of_bedrooms=4, no_of_bathrooms=1, address='18 Powell Street, San Francisco, CA', zip_code=94111, office = 3))
session.add(House(no_of_bedrooms=3, no_of_bathrooms=1, address='1 Found Street, San Mateo, CA', zip_code=11010, office = 1))
session.add(House(no_of_bedrooms=4, no_of_bathrooms=2, address='1 Market Street, San Francisco, CA', zip_code=94110, office = 3))
session.add(House(no_of_bedrooms=6, no_of_bathrooms=6, address='34 Post Street, Santa Clara, CA', zip_code=76110, office = 5))

session.add(Listing(house_id=1, seller_id=1, listing_date=datetime(2022, 1, 1), 
                    listing_agent_id=1, listing_office_id=1, listing_price=513467,
                    listing_state='AVAILABLE'))
session.add(Listing(house_id=2, seller_id=2, listing_date=datetime(2022, 2, 5),
                    listing_agent_id=2, listing_office_id=2, listing_price=1748361,
                    listing_state='AVAILABLE'))

session.add(Listing(house_id=3, seller_id=3, listing_date=datetime(2022, 3, 12),
                    listing_agent_id=3, listing_office_id=3, listing_price=316942,
                    listing_state='AVAILABLE'))

session.add(Listing(house_id=4, seller_id=3, listing_date=datetime(2022, 4, 20),
                    listing_agent_id=4, listing_office_id=4, listing_price=2216547,
                    listing_state='AVAILABLE'))

session.add(Listing(house_id=5, seller_id=1, listing_date=datetime(2022, 5, 25),
                    listing_agent_id=2, listing_office_id=5, listing_price=4592805,
                    listing_state='AVAILABLE'))

session.add(Listing(house_id=6, seller_id=2, listing_date=datetime(2022, 6, 29),
                    listing_agent_id=5, listing_office_id=6, listing_price=917103,
                    listing_state='AVAILABLE'))

session.add(Listing(house_id=7, seller_id=2, listing_date=datetime(2022, 7, 10),
                    listing_agent_id=1, listing_office_id=7, listing_price=1289412,
                    listing_state='AVAILABLE'))

session.add(Listing(house_id=8, seller_id=1, listing_date=datetime(2022, 8, 18),
                    listing_agent_id=3, listing_office_id=8, listing_price=674512,
                    listing_state='AVAILABLE'))

session.add(SalePriceSummary(total_sale=0))

session.commit()


def update_sales_info(sale):
    try:
        _extracted_from_update_sales_info_3(sale)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# TODO Rename this here and in `update_sales_info`
def _extracted_from_update_sales_info_3(sale):
    house_id = sale['house_id']
    house = session.query(Listing).filter_by(house_id=house_id).first()

    if house.listing_state == 'UNAVAILABLE':
        raise ValueError(f"House {house_id} is unavailable and cannot be sold.")

    session.execute(insert(Sale), [sale])
    session.query(Listing).filter(Listing.house_id == house_id).update(
        {Listing.listing_state: 'SOLD'}, synchronize_session=False)
    session.query(SalePriceSummary).filter(SalePriceSummary.id == 1).update(
        {SalePriceSummary.total_sale: SalePriceSummary.total_sale + sale['sale_price']}, 
        synchronize_session=False)
    session.commit()


sale = [
    {'buyer_id': 1,
    'sale_price': 597022, 
    'sell_date': datetime(2023, 8, 7), 
    'agent_id': 3,
    'house_id': 1},
    {'buyer_id': 4,
    'sale_price': 3745689,
    'sell_date': datetime(2023, 1, 12),
    'agent_id': 6,
    'house_id': 7},
    {'buyer_id': 2,
    'sale_price': 856739,
    'sell_date': datetime(2023, 2, 5),
    'agent_id': 5,
    'house_id': 5},
    {'buyer_id': 3,
    'sale_price': 2897432,
    'sell_date': datetime(2023, 1, 18),
    'agent_id': 1,
    'house_id': 3},
    {'buyer_id': 1,
    'sale_price': 4582273, 
    'sell_date': datetime(2023, 1, 23), 
    'agent_id': 4,
    'house_id': 1},
    {'buyer_id': 5,
    'sale_price': 1827949,
    'sell_date': datetime(2023, 1, 30),
    'agent_id': 3,
    'house_id': 8},
    {'buyer_id': 4,
    'sale_price': 3729845,
    'sell_date': datetime(2023, 1, 15),
    'agent_id': 2,'house_id': 6}
    ]

for i in sale:
    update_sales_info(i)

session.commit()


print(session.query(Customer).all())
print(session.query(Agent).all())
print(session.query(Office).all())
print(session.query(AgentOffice).all())
print(session.query(House).all())
print(session.query(Listing).all())
print(session.query(Sale).all())
print(session.query(SalePriceSummary).all())

#session.close()