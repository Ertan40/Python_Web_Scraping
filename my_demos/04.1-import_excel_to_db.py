import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, MetaData, DECIMAL
from sqlalchemy.exc import SQLAlchemyError

# Read Excel file into a DataFrame
df = pd.read_excel('SampleData.xlsx')
# print(df.head())
df.columns = ['OrderDate', 'Region', 'Rep', 'Item', 'Units', 'Unit_Cost', 'Total']

try:
    # Create SQLAlchemy engine
    engine = create_engine('postgresql+psycopg2://postgres-user:password@127.0.0.1:5432/sales_db')

    # Define table metadata
    metadata = MetaData()

    sales_table = Table(
        'sales', metadata,
        Column('id', Integer, primary_key=True),
        Column('OrderDate', Date),
        Column('Region', String(20)),
        Column('Rep', String(30)),
        Column('Item', String(30)),
        Column('Units', Integer),
        Column('Unit Cost', DECIMAL(10, 2)),
        Column('Total', DECIMAL(10, 2))
    )

    # Create the table if it doesn't exist
    metadata.create_all(engine)

    # Insert data into the table
    df.to_sql('sales', engine, if_exists='append', index=False, method='multi')

    print("Data imported successfully into PostgreSQL database.")

except SQLAlchemyError as e:
    print(f"An error occurred: {e}")


## tested via below query:
# SELECT "Region", round(AVG("Unit_Cost"), 2) AS "Average_Unit_Cost"
# FROM sales
# GROUP BY "Region"
# ORDER BY "Average_Unit_Cost";

## output:
# "East"	9.14
# "Central"	18.02
# "West"	53.66





