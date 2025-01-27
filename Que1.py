# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from sqlalchemy import create_engine
# import logging

# # Set up logging
# logging.basicConfig(filename='scraping_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# # Constants
# URL = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
# EURO_RATE = 0.93
# POUND_RATE = 0.8
# INR_RATE = 82.95
# DATABASE_NAME = 'banks'
# TABLE_NAME = 'Largest Banks'
# POSTGRES_USER = 'postgres'
# POSTGRES_PASSWORD = 'lucy'
# POSTGRES_HOST = 'localhost'
# POSTGRES_PORT = '5432'

# try:
#     # Scrape the data
#     logging.info("Starting to scrape the data from the website.")
#     response = requests.get(URL)
#     response.raise_for_status()  # Raise exception for HTTP errors
#     soup = BeautifulSoup(response.content, 'html.parser')
#     table = soup.find('table', {'class': 'wikitable'})
#     if table is None:
#         logging.error("Table not found on the webpage.")
#         raise ValueError("Table not found on the webpage.")

#     # Parse the table
#     from io import StringIO
#     df = pd.read_html(StringIO(str(table)))[0]

#     # Check if columns are multi-level and drop the first level if necessary
#     if isinstance(df.columns, pd.MultiIndex):
#         df.columns = df.columns.droplevel(0)

#     # Print column names to debug
#     print(df.columns)
#     df = df[['Bank name', 'Market cap (US$ billion)']]

#     # Rename columns for consistency
#     df.rename(columns={'Bank name': 'Bank Name', 'Market cap (US$ billion)': 'Market Cap (USD Billion)'}, inplace=True)

#     # Convert market capitalization to different currencies
#     df['Market Cap (Euro Billion)'] = (df['Market Cap (USD Billion)'] * EURO_RATE).round(2)
#     df['Market Cap (Pound Billion)'] = (df['Market Cap (USD Billion)'] * POUND_RATE).round(2)
#     df['Market Cap (INR Billion)'] = (df['Market Cap (USD Billion)'] * INR_RATE).round(2)

#     # Save to CSV
#     csv_file = 'largest_banks.csv'
#     df.to_csv(csv_file, index=False)
#     logging.info(f"Data saved to CSV file: {csv_file}")

#     # Connect to PostgreSQL and create database if it doesn't exist
#     engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}')
#     conn = engine.connect()
#     conn = conn.execution_options(isolation_level="AUTOCOMMIT")  # Set isolation level to AUTOCOMMIT
#     try:
#         conn.execute(f"CREATE DATABASE {DATABASE_NAME} WITH OWNER = {POSTGRES_USER} ENCODING = 'UTF8' CONNECTION LIMIT = -1;")
#         logging.info(f"Database {DATABASE_NAME} created successfully.")
#     except Exception as e:
#         logging.info(f"Database {DATABASE_NAME} already exists. Skipping creation.")
#     finally:
#         conn.close()

#     # Reconnect to the specific database
#     engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}')
#     logging.info(f"Connecting to the database {DATABASE_NAME}.")

#     # Check if the table exists and replace it
#     df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False)
#     logging.info(f"Data loaded to the database table {TABLE_NAME}.")
#     print("Process completed successfully!")

# except Exception as e:
#     logging.error(f"An error occurred: {e}")
#     print(f"An error occurred: {e}")