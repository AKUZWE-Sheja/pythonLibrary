from sqlalchemy import create_engine
import pandas as pd

db_user: str = 'postgres'
db_port: int = 4221
db_host: str = 'localhost'
db_password: str = 'Edwige_sroot'

# Connection strings for both databases
db1_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/eb_ml"

# Create database engines
engine_db1 = create_engine(db1_url) # create_engine() func to connect to a PostgreSQL database by passing a connection string that includes the database name, username, password, host, and port.

# Example: Fetch data into DataFrames
query_db1 = "SELECT * FROM library_books;"
query_db2 = "SELECT * FROM authors;"

df_books = pd.read_sql(query_db1, engine_db1)
df_authors = pd.read_sql(query_db1, engine_db1)

# Offline access, portability & quick debug
df_books.to_csv('books_data.csv', index=False)
df_authors.to_csv('authors_data.csv', index=False)
# print("Data exported to books_data.csv and authors_data.csv!")

# Load the CSVs
books_data = pd.read_csv('books_data.csv')
authors_data = pd.read_csv('authors_data.csv')

# print(books_data.head())
# print(authors_data.head())

# print(books_data.isnull().sum())
# print(authors_data.isnull().sum())

# Handling the nulls
'''1. FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.'''
# authors_data['bio'] = authors_data['bio'].astype('object').fillna('A bestselling author')
authors_data.dropna(axis=1, how='all', inplace=True) # axis=1: Operates on columns (rows is 0), inplace=True: Modifies the original DataFrame
# print(authors_data.isnull().sum())

df_merged1 = pd.merge(books_data, authors_data, on='author_id', how='inner')  # 'left', 'right', 'outer' if needed
df_merged1.to_csv('merged_inner.csv', index=False)
merged_inner = pd.read_csv('merged_inner.csv')
print(merged_inner.head(2))
# print(merged_inner.info())

df_merged2 = pd.merge(books_data, authors_data, on='author_id', how='left')
df_merged2.to_csv('merged_left.csv', index=False)
merged_left = pd.read_csv('merged_left.csv')
print(merged_left.head(2))

df_merged3 = pd.merge(books_data, authors_data, on='author_id', how='right')
df_merged3.to_csv('merged_right.csv', index=False)
merged_right = pd.read_csv('merged_right.csv')
print(merged_right.head(2))

# encoded_df = pd.get_dummies(merged_lib, columns=['category'], prefix='cat', prefix_sep='-')
# print(encoded_df.head())

# Count books by authors
# books_per_author = merged_lib.groupby('name')['book_id'].count()
# print(books_per_author)






