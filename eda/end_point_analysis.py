import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

url = "http://localhost:8000/"
endpoint1 = "authors"
endpoint2 = "books"

# Define the API endpoints
authors_url = f"{url}/{endpoint1}/"
books_url = f"{url}/{endpoint2}/"

# Fetch data from endpoints
authors_res = requests.get(authors_url)
books_res = requests.get(books_url)

# Converting the responses I got to DataFrames
authors_data = pd.DataFrame(authors_res.json())
books_data = pd.DataFrame(books_res.json())

# Merge DataFrames on author_id
df_merged = pd.merge(books_data, authors_data, left_on='author_id', right_on='author_id', how='inner')
# the merges are all going to be the same since all my data goes with each other, each books has a known author

# Handle nulls by filling - literally dropping them rn
df_merged.dropna(axis=1, how='all', inplace=True) # axis=1: Operates on columns (rows is 0), inplace=True: Modifies the original DataFrame

print(df_merged.isnull().sum())

# Select only numeric columns for correlation matrix 
numeric_df = df_merged.select_dtypes(include=['float64', 'int64'])

#  The correlation matrix
corr_matrix = numeric_df.corr()
print(corr_matrix)

# Identify perfect positive correlations - the 1s
perfect_positive_corrs = []
for col in corr_matrix.columns:
    for index in corr_matrix.index:
        if col != index and corr_matrix.at[index, col] == 1.0:
            perfect_positive_corrs.append((index, col))

# Print the results
for pair in perfect_positive_corrs:
    print(f"{pair[0]} and {pair[1]} are perfectly positively correlated.")

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Some other manipulations
encoded_df = pd.get_dummies(df_merged, columns=['category'], prefix='cat', prefix_sep='-')
print(encoded_df.head())

# Count books by authors
books_per_author = df_merged.groupby('name')['book_id'].count()
print(books_per_author)

category_counts = df_merged['category'].value_counts()

# Bar plot for book counts by category
plt.figure(figsize=(7, 4))
sns.barplot(x=category_counts.index, y=category_counts.values, palette='viridis')
plt.title('Number of Books per Category', fontsize=12)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Group by year and count books
books_per_year = df_merged.groupby('year').size()

# Line plot for books per year
plt.figure(figsize=(8, 4))
books_per_year.plot(kind='line', marker='o', color='teal')
plt.title('Number of Books Published per Year', fontsize=12)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Books', fontsize=12)
plt.grid(True)
plt.show()