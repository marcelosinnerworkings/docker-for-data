'''
This script may run either inside or outside a Docker container, but
the first case is simpler if you are familiar with Docker use and want
to avoid configuring or installing dependencies.

After confirmation that this repository was cloned to the local machine
and Docker daemon is running, execute the following commands inside
this folder, using the terminal:

---

docker build -t scripter .

(wait for the build to finish)

docker run -v .:/scripter scripter

---

The CSV file will be "spilled" to the same directory where these files
are.

'''

import sqlalchemy
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Database environment variables
# Remember to change the table name accordingly
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_table_name = os.getenv('DB_TABLE_NAME')

# Database connection parameters
db_params = {
    'database': db_name,
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'port': db_port
}

csv_file_name = 'csv_cutie_file.csv'

try:
    # The example below is for a Postgres database
    # Remember to check the precise SQL syntax, as it varies according to the database
    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
    )

    df = pd.read_sql(f'SELECT * FROM "public"."{db_table_name}"', engine)

    df.to_csv(csv_file_name, index=False)

    print(f'Data from table {db_table_name} has been exported to {csv_file_name}')

except Exception as e:
    print(f'Error: {e}')

