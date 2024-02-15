import pandas as pd

# Example DataFrame
data = {'A': [5, 15, 20],
        'B': [10, 10, 10]}
df = pd.DataFrame(data)

# Using boolean indexing
filtered_df = df['A']

# Display the filtered DataFrame
print(filtered_df)
