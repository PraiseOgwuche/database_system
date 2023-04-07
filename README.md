# Real Estate Head Office Database
A database application created using SQL, SQLAlchemy and Python for the database system of the Real Estate Head Office. It contains all data pertaining to the listings, sales, agents, customers etc. Data can be inserted, and queried from the database.

Running locally
---------------
The application can be run with the following steps:

 1. Create a virtual environment
 
        python3 -m venv venv
       
 2. Activate the virtual environment
 
     On mac:
     
        source venv/bin/activate
        
     On windows:
     
        venv\Scripts\activate.bat
        
 3. Install required python packages:

        pip install -r requirements.txt

 4. Running the database (this prints out the outputs):

        python3 create.py
        python3 insert_data.py
        python3 query_data.py

 5. Reading the SQL files:
 
        .read create.sql
        .read insert_data.sql
        .read query_data.sql
        
