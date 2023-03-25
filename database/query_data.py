from datetime import datetime
from sqlalchemy import create_engine, func, desc, case, cast, Integer, and_
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import extract, select
from create import House, Listing, Office, Agent, Customer, Sale

engine = create_engine('sqlite:///database.db')
engine.connect()

Session = sessionmaker(bind=engine)
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
print('Find the top 5 estate agents who have sold the least for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).')
print('"""')
print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
    Sale, Sale.listing_id == Listing.id).filter(extract('month', Sale.sell_date) == datetime.now().month).group_by(Agent.id).order_by(func.sum(Sale.sell_price_IN_CENTS)).all())

print('"""')
print('Find the top 5 estate agents who have sold the most for the year (include their contact details and their sales details so that it is easy contact them and congratulate them).')
print('"""')
print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
    Sale, Sale.listing_id == Listing.id).filter(extract('year', Sale.sell_date) == datetime.now().year).group_by(Agent.id).order_by(desc(func.sum(Sale.sell_price_IN_CENTS))).all())

print('"""')
print('Find the top 5 estate agents who have sold the least for the year (include their contact details and their sales details so that it is easy contact them and congratulate them).')
print('"""')
print(session.query(Agent.firstName, Agent.lastName, Agent.emailAddress, Sale.sell_price_IN_CENTS, Sale.sell_date).join(Listing, Listing.listing_agent_id == Agent.id).join(
    Sale, Sale.listing_id == Listing.id).filter(extract('year', Sale.sell_date) == datetime.now().year).group_by(Agent.id).order_by(func.sum(Sale.sell_price_IN_CENTS)).all())

print('"""')
print('Calculate the commission that each estate agent must receive and store the results in a separate table.')
print('"""')
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
