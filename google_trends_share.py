from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Initialize pytrends and set to UK and GMT Timezone
pytrends = TrendReq(hl='en-GB', tz=0)

# Search Terms List
kw_list = ["Football", "Rugby", "Tennis"]

# Payload
pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='', gprop='')

# Retrieve interest over time
df = pytrends.interest_over_time()

# Drop the 'isPartial' column if it exists - not needed.
if 'isPartial' in df.columns:
    df = df.drop(columns=['isPartial'])

# Check the df
print(df.head())

# Search Term Interest Over Time - Independent
df.plot()
plt.title('Search Term Interest Over 3 Months')
plt.xlabel('Date')
plt.ylabel('Search Interest')
plt.legend(title='Search Terms')
plt.show()

# Search Term's Relative Share
# 'Share' here is interpreted as 'the share of interest each term has relative to the other terms selected'

# Simple sum to get total across search terms.
df['Total'] = df[kw_list].sum(axis=1)

# Get Share (%) of each term relative to others
for term in kw_list:
    df[f'{term} Share'] = (df[term] / df['Total']) * 100
    df = df.round({f'{term} Share': 2})
    df.drop([term], axis=1, inplace=True)

# Check the df
print(df.head())

df.drop(['Total'], axis=1, inplace=True)

# Search Term Interest Over Time - Share
df.plot.area(stacked=False)
plt.title('Search Term Share Over 3 Months')
plt.xlabel('Date')
plt.ylabel('Search Share (%)')
plt.legend(title='Search Terms')
plt.show()
