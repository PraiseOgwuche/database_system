import unittest
from create import House, Listing, Office, Agent, Customer, Sale, AgentCommission, AgentOffice, SalePriceSummary, Base, engine 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import insert_data
import query_data

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def test_database(self):
        house = House(no_of_bedrooms=3, no_of_bathrooms=2, address="123 Main St", zip_code=12345, office = 2)
        self.session.add(house)
        self.session.commit()
        self.assertEqual(house.id, 1)
        self.assertEqual(house.no_of_bedrooms, 3)
        self.assertEqual(house.no_of_bathrooms, 2)
        self.assertEqual(house.address, "123 Main St")
        self.assertEqual(house.zip_code, 12345)
        self.assertEqual(house.office, 2)

        office = Office(office_name="san francisco")
        self.session.add(office)
        self.session.commit()
        self.assertEqual(office.id, 1)
        self.assertEqual(office.office_name, "san francisco")

        listing = Listing(house_id=1, seller_id=1, listing_date= datetime(2022, 6, 29), listing_agent_id=1, listing_office_id=1, listing_price=100000, listing_state = 'AVAILABLE')
        self.session.add(listing)
        self.session.commit()
        self.assertEqual(listing.id, 1)
        self.assertEqual(listing.house_id, 1)
        self.assertEqual(listing.seller_id, 1)
        self.assertEqual(listing.listing_date, datetime(2022, 6, 29))
        self.assertEqual(listing.listing_agent_id, 1)
        self.assertEqual(listing.listing_office_id, 1)
        self.assertEqual(listing.listing_price, 100000)
        self.assertEqual(listing.listing_state, "AVAILABLE")

        sale = Sale(listing_id=1, buyer_id=1, sale_price=100000, sell_date=datetime(2023, 2, 5))
        self.session.add(sale)
        self.session.commit()
        self.assertEqual(sale.id, 1)
        self.assertEqual(sale.listing_id, 1)
        self.assertEqual(sale.buyer_id, 1)
        self.assertEqual(sale.sale_price, 100000)


        agent = Agent(firstName='John', lastName='Ezra', emailAddress='test@example.com')
        self.session.add(agent)
        self.session.commit()
        self.assertEqual(agent.id, 1)
        self.assertEqual(agent.firstName, 'John')
        self.assertEqual(agent.lastName, 'Ezra')
        self.assertEqual(agent.emailAddress, 'test@example.com')

        customer = Customer(firstName='Praise', lastName='Ogwuche', emailAddress='praiseogwuche@staple.com')
        self.session.add(customer)
        self.session.commit()
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.firstName, 'Praise')
        self.assertEqual(customer.lastName, 'Ogwuche')
        self.assertEqual(customer.emailAddress, 'praiseogwuche@staple.com')

        agent_commission = AgentCommission(agent_id=1, monthly_commission=10000)
        self.session.add(agent_commission)
        self.session.commit()
        self.assertEqual(agent_commission.id, 1)
        self.assertEqual(agent_commission.agent_id, 1)
        self.assertEqual(agent_commission.monthly_commission, 10000)

        agent_office = AgentOffice(agent_id=1, office_id=1)
        self.session.add(agent_office)
        self.session.commit()
        self.assertEqual(agent_office.id, 1)
        self.assertEqual(agent_office.agent_id, 1)
        self.assertEqual(agent_office.office_id, 1)
        
        sale_price_summary = SalePriceSummary(total_sale = 3729845)
        self.session.add(sale_price_summary)
        self.session.commit()
        self.assertEqual(sale_price_summary.id, 1)
        self.assertEqual(sale_price_summary.total_sale, 3729845)



    # def tearDown(self):
    #     self.session.close()
    #     self.engine.dispose()


if __name__ == '__main__':
    unittest.main()
