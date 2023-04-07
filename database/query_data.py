from datetime import date, datetime
from sqlalchemy import create_engine, func, desc, case, cast, Integer, and_, extract, insert, join, distinct
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import extract, select
from create import House, Listing, Office, Agent, Customer, Sale, AgentCommission, AgentOffice, SalePriceSummary, Base, engine 
from sqlalchemy.sql.expression import desc
from faker import Faker
from sqlalchemy import Index
import insert_data

Session = sessionmaker(bind=engine)
session = Session()

year = 2023
month = 1
print('For year', year, 'month', month)
# 1. Find the top 5 offices with the most Sale for that month.
# create index
# 1. Find the top 5 offices with the most Sale
idx1 = Index("offices' id", House.office, House.id)
idx2 = Index("sell_date_price", Sale.sell_date, Sale.sale_price)

result1 = session.query(
    Office.office_name, func.sum(Sale.sale_price).label('office_sale')).filter(
    extract('year', Sale.sell_date) == year, extract('month', Sale.sell_date) == month).join(
    House,House.id == Sale.house_id).join(
    Office,Office.id == House.office).group_by(
    House.office).order_by(func.sum(Sale.sale_price).desc()).limit(5).all()

print('The top five offices with the most sales are:')
for office_name, total_sales in result1:
    print(f'{office_name}: {total_sales}')
try:
    assert result1[3] == ('santa clara', 1827949)
    assert result1[0] == ('san jose', 8327962)
except AssertionError as e:
    print("Assertion Error:", e)

# 2. Find the top 5 estate agents who have sold the most
idx3 = Index("agent's id", Sale.agent_id)

result2 = session.query(
    Agent.firstName, Agent.lastName, Agent.emailAddress, func.sum(Sale.sale_price).label("Amount_sold")
).filter(
    extract('year', Sale.sell_date) == year, extract('month', Sale.sell_date) == month
).join(
    Agent,Agent.id == Sale.agent_id
).group_by(
    Sale.agent_id
).order_by(
    func.sum(Sale.sale_price).desc()
).limit(5).all()

print('The top 5 estate agents who have sold the most are:')
for first_name, last_name, email, amount_sold in result2:
    print(f'{first_name} {last_name} ({email}): {amount_sold}')

#Find the top 5 estate agents who have sold the most for the year
idx8 = Index("agent id", Sale.agent_id)

result8 = session.query(
    Agent.firstName, Agent.lastName, Agent.emailAddress, func.sum(Sale.sale_price).label("Amount_sold")
).filter(
    extract('year', Sale.sell_date) == year
).join(
    Agent,Agent.id == Sale.agent_id
).group_by(
    Sale.agent_id
).order_by(
    func.sum(Sale.sale_price).desc()
).limit(5).all()

print('The top 5 estate agents who have sold the most for the year are:')
for first_name, last_name, email, amount_sold in result8:
    print(f'{first_name} {last_name} ({email}): {amount_sold}')


# 3. Calculate the commission that each estate agent must receive and store the results in a separate table.
idx4 = Index("agent's commission", Sale.agent_commissions)

sel = session.query(Sale.agent_id, func.sum(Sale.agent_commissions).label("Total_commission")).filter(
    extract('year', Sale.sell_date) == year, extract('month', Sale.sell_date) == month).group_by(
    Sale.agent_id)
i = insert(AgentCommission).from_select(names=['agent_id', 'monthly_commission'],
                                           select=sel)
session.execute(i)

result3 = session.query(AgentCommission).all()

print('The commission for each agent is:')
for agent_commission in result3:
    print(f'{agent_commission.agent_id}: {agent_commission.monthly_commission}')

# 4. For all houses that were sold that month, calculate the average number of days that the house was on the market.
'''
sql
SELECT AVG(Sale.sell_date - Listing.date) FROM Sale
WHERE date = datetime(2018,1)
JOIN Listing
ON Listing.house_id = Sale.house_id
'''

result_avg_days = session.query(func.avg(func.julianday(Sale.sell_date) - func.julianday(Listing.listing_date))).filter(
extract('year', Sale.sell_date) == year, extract('month', Sale.sell_date) == month).join(
Listing, Listing.house_id == Sale.house_id).first()

assert result_avg_days[0] == 250
print(f"The average number of days that the house was on the market is: {result_avg_days[0]} days")

# 5. For all houses that were sold that month, calculate the average selling price
'''
sql
SELECT avg(Sale.sale_price) FROM Sale
WHERE date = datetime(2018,1)
'''

result_avg_price = session.query(func.avg(Sale.sale_price)).filter(
extract('year', Sale.sell_date) == year, extract('month', Sale.sell_date) == month).first()

assert result_avg_price[0] == 3356637.6

print(f"The average selling price for all houses is: ${result_avg_price[0]:,.2f}")
# 6. Find the zip codes with the top 5 average Sale prices
'''
sql
SELECT House.zip_code, avg(Sale.sale_price) from Sale
JOIN House
ON House.house_id = Sale.house_id
WHERE date = datetime(2018,1)
GROUP BY House.zip_code
'''

result_top_zipcodes = session.query(House.zip_code, func.avg(Sale.sale_price)).join(
House, House.id == Sale.house_id).filter(
extract('year', Sale.sell_date) == year, extract('month', Sale.sell_date) == month).group_by(
House.zip_code).order_by(func.avg(Sale.sale_price).desc()).limit(5).all()

assert result_top_zipcodes[0] == (94111, 4582273.0)
print("The zip codes with the top 5 average Sale prices are:")
for index, (zip_code, avg_price) in enumerate(result_top_zipcodes, start=1):
    print(f"{index}. {zip_code}: ${avg_price:,.2f}")