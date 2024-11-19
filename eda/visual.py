import matplotlib.pyplot as plt
import seaborn as sns
from analysis import merged_lib

# Count books per category
category_counts = merged_lib['category'].value_counts()

# Bar plot for book counts by category
plt.figure(figsize=(7, 4))
sns.barplot(x=category_counts.index, y=category_counts.values, palette='viridis')
plt.title('Number of Books per Category', fontsize=12)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Group by year and count books
books_per_year = merged_lib.groupby('year').size()

# Line plot for books per year
plt.figure(figsize=(8, 4))
books_per_year.plot(kind='line', marker='o', color='teal')
plt.title('Number of Books Published per Year', fontsize=12)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Books', fontsize=12)
plt.grid(True)
plt.show()
