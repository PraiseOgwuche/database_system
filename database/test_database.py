import unittest
from create import Base, House, Office, Listing, Sale
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def test_database(self):
        house = House(no_of_bedrooms=3, no_of_bathrooms=2, address="123 Main St", zip_code="12345")
        self.session.add(house)
        self.session.commit()
        self.assertEqual(house.id, 1)
        self.assertEqual(house.no_of_bedrooms, 3)
        self.assertEqual(house.no_of_bathrooms, 2)
        self.assertEqual(house.address, "123 Main St")
        self.assertEqual(house.zip_code, "12345")

        office = Office(location="123 Main St")
        self.session.add(office)
        self.session.commit()
        self.assertEqual(office.id, 1)
        self.assertEqual(office.location, "123 Main St")

        listing = Listing(house_id=1, seller_id=1, listing_agent_id=1, listing_office_id=1, listing_price_IN_CENTS=100000)
        self.session.add(listing)
        self.session.commit()
        self.assertEqual(listing.id, 1)
        self.assertEqual(listing.house_id, 1)
        self.assertEqual(listing.seller_id, 1)
        self.assertEqual(listing.listing_agent_id, 1)
        self.assertEqual(listing.listing_office_id, 1)
        self.assertEqual(listing.listing_price_IN_CENTS, 100000)
        self.assertEqual(listing.listing_state, "AVAILABLE")

        sale = Sale(listing_id=1, buyer_id=1, sell_price_IN_CENTS=100000, sell_date=datetime.now())
        self.session.add(sale)
        self.session.commit()
        self.assertEqual(sale.id, 1)
        self.assertEqual(sale.listing_id, 1)
        self.assertEqual(sale.buyer_id, 1)
        self.assertEqual(sale.sell_price_IN_CENTS, 100000)
        #self.assertEqual(sale.sell_date, datetime.now())
    
    # def tearDown(self):
    #     self.session.close()
    #     self.engine.dispose()


if __name__ == '__main__':
    unittest.main()
