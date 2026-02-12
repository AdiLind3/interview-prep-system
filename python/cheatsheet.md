# Python & Pandas Cheat Sheet for Data Engineering

## Table of Contents
- [Python Essentials](#python-essentials)
- [Pandas DataFrames](#pandas-dataframes)
- [Data Transformation](#data-transformation)
- [Aggregation & Grouping](#aggregation--grouping)
- [Joining & Merging](#joining--merging)
- [Time Series](#time-series)
- [Performance Tips](#performance-tips)
- [Common Patterns](#common-patterns)

---

## Python Essentials

### List Comprehensions
```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Nested
matrix = [[i+j for j in range(3)] for i in range(3)]

# Flattening
nested = [[1, 2], [3, 4], [5]]
flat = [item for sublist in nested for item in sublist]
```

### Dictionary Comprehensions
```python
# Basic
squares_dict = {x: x**2 for x in range(5)}

# From lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}

# Filtering
filtered = {k: v for k, v in data.items() if v > 100}

# Transformation
upper_dict = {k.upper(): v for k, v in data.items()}
```

### Set Operations
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

union = a | b  # or a.union(b)
intersection = a & b  # or a.intersection(b)
difference = a - b  # or a.difference(b)
symmetric_diff = a ^ b  # or a.symmetric_difference(b)

# Check membership
is_subset = a <= b
is_superset = a >= b
```

### Lambda Functions
```python
# Basic
square = lambda x: x**2

# With multiple args
add = lambda x, y: x + y

# In sorted
data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
sorted_data = sorted(data, key=lambda x: x['age'])

# In map
numbers = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, numbers))

# In filter
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

### Error Handling
```python
# Basic try-except
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")

# Multiple exceptions
try:
    value = data[key]
except (KeyError, IndexError, TypeError) as e:
    print(f"Error: {e}")

# With finally
try:
    file = open('data.txt')
    data = file.read()
finally:
    file.close()

# With else
try:
    result = process_data()
except Exception as e:
    handle_error(e)
else:
    # Runs if no exception
    save_result(result)
```

### Context Managers
```python
# File handling
with open('file.txt', 'r') as f:
    data = f.read()

# Multiple contexts
with open('input.txt') as f_in, open('output.txt', 'w') as f_out:
    f_out.write(f_in.read())

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"Took {time.time() - start:.2f}s")

with timer():
    expensive_operation()
```

---

## Pandas DataFrames

### Creating DataFrames
```python
import pandas as pd

# From dict
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NY', 'SF', 'LA']
})

# From list of dicts
data = [
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30}
]
df = pd.DataFrame(data)

# From CSV
df = pd.read_csv('data.csv')

# From JSON
df = pd.read_json('data.json')

# From SQL
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM table', conn)
```

### Basic Operations
```python
# Info about DataFrame
df.shape  # (rows, columns)
df.info()  # Column types and nulls
df.describe()  # Statistical summary
df.head(10)  # First 10 rows
df.tail(10)  # Last 10 rows

# Column operations
df.columns  # Column names
df.dtypes  # Column types
df.rename(columns={'old': 'new'})
df.drop(columns=['col1', 'col2'])

# Row operations
len(df)  # Number of rows
df.drop(index=[0, 1, 2])
df.reset_index(drop=True)
```

### Selecting Data
```python
# Select columns
df['name']  # Single column (Series)
df[['name', 'age']]  # Multiple columns (DataFrame)

# loc: label-based
df.loc[0]  # Row by index
df.loc[0:5]  # Rows 0 to 5 (inclusive)
df.loc[df['age'] > 25]  # Boolean indexing
df.loc[df['age'] > 25, ['name', 'age']]  # Rows and columns

# iloc: position-based
df.iloc[0]  # First row
df.iloc[0:5]  # First 5 rows (exclusive)
df.iloc[:, 0:3]  # All rows, first 3 columns
df.iloc[0, 0]  # Single value

# at & iat: single value access
df.at[0, 'name']  # Fast label-based
df.iat[0, 0]  # Fast position-based
```

### Filtering
```python
# Boolean indexing
df[df['age'] > 25]
df[df['city'] == 'NY']
df[df['name'].isin(['Alice', 'Bob'])]
df[df['name'].str.contains('Ali')]

# Multiple conditions
df[(df['age'] > 25) & (df['city'] == 'NY')]
df[(df['age'] < 20) | (df['age'] > 60)]
df[~df['city'].isin(['NY', 'SF'])]  # NOT

# query method
df.query('age > 25 and city == "NY"')
```

---

## Data Transformation

### Adding/Modifying Columns
```python
# Simple assignment
df['age_in_months'] = df['age'] * 12

# Apply function
df['name_upper'] = df['name'].apply(lambda x: x.upper())
df['name_upper'] = df['name'].str.upper()  # String method

# Apply with multiple columns
df['full_name'] = df.apply(
    lambda row: f"{row['first']} {row['last']}",
    axis=1
)

# Map values
mapping = {'M': 'Male', 'F': 'Female'}
df['gender_full'] = df['gender'].map(mapping)

# np.where (vectorized if-else)
import numpy as np
df['age_group'] = np.where(df['age'] < 30, 'Young', 'Old')

# Multiple conditions
df['category'] = np.select(
    [df['score'] >= 90, df['score'] >= 75, df['score'] >= 60],
    ['A', 'B', 'C'],
    default='F'
)
```

### Handling Missing Data
```python
# Check for nulls
df.isnull()  # or df.isna()
df.isnull().sum()  # Count per column
df.isnull().any()  # Any nulls?

# Drop nulls
df.dropna()  # Drop rows with any null
df.dropna(subset=['col1', 'col2'])  # Drop if null in specific columns
df.dropna(axis=1)  # Drop columns with any null
df.dropna(thresh=3)  # Keep rows with at least 3 non-null values

# Fill nulls
df.fillna(0)  # Fill with constant
df.fillna(method='ffill')  # Forward fill
df.fillna(method='bfill')  # Backward fill
df['age'].fillna(df['age'].mean())  # Fill with mean
df.fillna(df.median())  # Fill with median per column
```

### Sorting
```python
# Sort by column
df.sort_values('age')
df.sort_values('age', ascending=False)

# Sort by multiple columns
df.sort_values(['city', 'age'], ascending=[True, False])

# Sort by index
df.sort_index()
```

---

## Aggregation & Grouping

### GroupBy Operations
```python
# Basic groupby
grouped = df.groupby('city')
grouped.size()  # Count per group
grouped.count()  # Non-null count per column
grouped.mean()  # Mean per group
grouped.sum()
grouped.min()
grouped.max()

# Multiple columns
df.groupby(['city', 'gender']).mean()

# Multiple aggregations
df.groupby('city').agg({
    'age': ['mean', 'min', 'max'],
    'salary': ['sum', 'mean']
})

# Named aggregations
df.groupby('city').agg(
    avg_age=('age', 'mean'),
    max_age=('age', 'max'),
    total_salary=('salary', 'sum')
)

# Custom aggregation
df.groupby('city')['age'].agg(lambda x: x.max() - x.min())

# Apply custom function to groups
def top_2_salaries(group):
    return group.nlargest(2, 'salary')

df.groupby('department').apply(top_2_salaries)
```

### Pivot Tables
```python
# Basic pivot
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='month',
    aggfunc='sum'
)

# Multiple aggregations
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='month',
    aggfunc=['sum', 'mean', 'count']
)

# Multiple values
pivot = df.pivot_table(
    values=['sales', 'profit'],
    index='product',
    columns='month',
    aggfunc='sum'
)

# With margins (totals)
pivot = df.pivot_table(
    values='sales',
    index='product',
    columns='month',
    aggfunc='sum',
    margins=True
)
```

---

## Joining & Merging

### Merge (SQL-style joins)
```python
# Inner join (default)
pd.merge(df1, df2, on='key')
pd.merge(df1, df2, on=['key1', 'key2'])

# Left join
pd.merge(df1, df2, on='key', how='left')

# Right join
pd.merge(df1, df2, on='key', how='right')

# Outer join
pd.merge(df1, df2, on='key', how='outer')

# Different column names
pd.merge(df1, df2, left_on='id', right_on='customer_id')

# On index
pd.merge(df1, df2, left_index=True, right_index=True)

# Indicator column
pd.merge(df1, df2, on='key', how='outer', indicator=True)
```

### Join (index-based)
```python
# Join on index
df1.join(df2)
df1.join(df2, how='left')

# Join on specific column
df1.set_index('key').join(df2.set_index('key'))
```

### Concat
```python
# Vertical concat (stacking)
pd.concat([df1, df2], axis=0)
pd.concat([df1, df2], ignore_index=True)  # Reset index

# Horizontal concat
pd.concat([df1, df2], axis=1)

# With keys
pd.concat([df1, df2], keys=['first', 'second'])
```

---

## Time Series

### Date Parsing
```python
# Parse dates
df['date'] = pd.to_datetime(df['date_string'])
df['date'] = pd.to_datetime(df['date_string'], format='%Y-%m-%d')

# Extract date parts
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek
df['quarter'] = df['date'].dt.quarter
df['weekofyear'] = df['date'].dt.isocalendar().week
```

### Time Operations
```python
# Set datetime index
df.set_index('date', inplace=True)

# Resample (time-based groupby)
df.resample('D').sum()  # Daily sum
df.resample('W').mean()  # Weekly mean
df.resample('M').sum()  # Monthly sum
df.resample('Q').sum()  # Quarterly sum

# Rolling windows
df['rolling_avg'] = df['value'].rolling(window=7).mean()
df['rolling_sum'] = df['value'].rolling(window=7).sum()

# Shift (lag/lead)
df['prev_value'] = df['value'].shift(1)  # Previous day
df['next_value'] = df['value'].shift(-1)  # Next day
df['diff'] = df['value'] - df['value'].shift(1)  # Day-over-day change

# Datetime arithmetic
df['next_week'] = df['date'] + pd.Timedelta(days=7)
df['last_month'] = df['date'] - pd.DateOffset(months=1)
```

---

## Performance Tips

### Vectorization
```python
# BAD: Looping
result = []
for value in df['column']:
    result.append(value * 2)
df['new_col'] = result

# GOOD: Vectorized
df['new_col'] = df['column'] * 2

# BAD: Apply with simple operation
df['new'] = df['col'].apply(lambda x: x * 2)

# GOOD: Vectorized
df['new'] = df['col'] * 2
```

### Memory Optimization
```python
# Check memory usage
df.memory_usage(deep=True)

# Downcast numeric types
df['int_col'] = pd.to_numeric(df['int_col'], downcast='integer')
df['float_col'] = pd.to_numeric(df['float_col'], downcast='float')

# Use categories for low-cardinality strings
df['category_col'] = df['category_col'].astype('category')

# Read CSV in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process(chunk)
```

### Efficient Reading
```python
# Specify dtypes when reading
dtypes = {'col1': 'int32', 'col2': 'category'}
df = pd.read_csv('data.csv', dtype=dtypes)

# Use columns parameter to read subset
df = pd.read_csv('data.csv', usecols=['col1', 'col2'])

# Use nrows for sampling
df = pd.read_csv('large.csv', nrows=1000)
```

---

## Common Patterns

### Deduplication
```python
# Drop duplicates
df.drop_duplicates()
df.drop_duplicates(subset=['col1', 'col2'])
df.drop_duplicates(keep='first')  # Keep first occurrence
df.drop_duplicates(keep='last')  # Keep last occurrence

# Check for duplicates
df.duplicated()
df.duplicated().sum()
```

### Value Counts
```python
# Count occurrences
df['column'].value_counts()
df['column'].value_counts(normalize=True)  # Percentages
df['column'].value_counts(dropna=False)  # Include NaN

# Cross-tabulation
pd.crosstab(df['col1'], df['col2'])
```

### Reshaping
```python
# Wide to long
df_long = df.melt(
    id_vars=['id', 'name'],
    value_vars=['Q1', 'Q2', 'Q3', 'Q4'],
    var_name='quarter',
    value_name='sales'
)

# Long to wide
df_wide = df_long.pivot(
    index='id',
    columns='quarter',
    values='sales'
)

# Stack/Unstack
df.stack()  # Columns to rows
df.unstack()  # Rows to columns
```

### Conditional Selection
```python
# Where (replace values not meeting condition)
df['col'].where(df['col'] > 0, 0)  # Replace negative with 0

# Mask (opposite of where)
df['col'].mask(df['col'] < 0, 0)  # Replace values < 0 with 0

# Clip (limit values)
df['col'].clip(lower=0, upper=100)  # Constrain between 0 and 100
```
