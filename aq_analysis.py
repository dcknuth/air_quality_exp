import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

aq = pd.read_csv('daily_88101_2022.csv')
# See what we have
for col in aq.columns:
    print(col)
state_codes = aq['State Code'].unique()
state_names = aq['State Name'].unique()
print(state_names[:7])
aq.head()
# Filer and save just CA data so we can work with a smaller set
ca = aq[aq['State Name'] == 'California']
ca.head()
bako = ca[ca['City Name'] == 'Bakersfield']
print(bako.iloc[0])
bako['Local Site Name'].unique()
# There are three Bakersfield sites. Let's break them out so we can see if the
#  data is collected evenly/regularly
bako_s1 = bako[bako['Local Site Name'] == 'Bakersfield-Golden / M St']
bako_s2 = bako[bako['Local Site Name'] == 'Bakersfield-California']
bako_s3 = bako[bako['Local Site Name'] == 'Bakersfield-Airport (Planz)']
bako_s2['Arithmetic Mean'].dtype
bako_s2['Date Local'].dtype
bako_s2['Date'] = pd.to_datetime(bako_s2.loc[:,'Date Local'], format='%Y-%m-%d')
bako_s2['Date'].head()
# Drop the other attempt to get a date column
#bako_s2.drop(columns='Date Type', inplace=True)
for col in bako_s2.columns:
    print(col)
bako_s2_mean_over_time = bako_s2.groupby('Date')['Arithmetic Mean'].mean()

plt.ioff()
sns.set_theme(style='whitegrid')
sns.relplot(data=bako_s2_mean_over_time,
            label='Average µg/m³ of 2.5 micron\nparticles for the day')
plt.xticks(rotation=45, ha='right')
# Line for good level at 12
plt.axhline(y=12, color='g', label='Air quality is good below this')
plt.axhline(y=30, color='r', label='Air quality is bad above this')
plt.legend()
plt.title('Air quality in Bakersfield')
plt.show()
# Interesting, air quality seems to be worse in the winter in Bako

# VS a few other cities
# san jose
sj = ca[ca['City Name'] == 'San Jose']
print(sj.iloc[0])
sj['Local Site Name'].unique()
print(sj[sj['Local Site Name'] == 'San Jose - Knox Avenue'].iloc[0])
sj['Date'] = pd.to_datetime(sj.loc[:,'Date Local'], format='%Y-%m-%d')
sj_stats = sj.groupby('Date')['Arithmetic Mean'].mean()
sns.relplot(data=sj_stats,
            label='Average µg/m³ of 2.5 micron\nparticles for the day')
plt.xticks(rotation=45, ha='right')
plt.axhline(y=12, color='g', label='Air quality is good below this')
plt.axhline(y=30, color='r', label='Air quality is bad above this')
plt.legend()
plt.title('Air quality in San Jose')
plt.show()
# St Paul
mn = aq[aq['State Name'] == 'Minnesota']
for city in mn['City Name'].unique():
    print(city)
mn_sp = mn[mn['City Name'] == 'St. Paul']
mn_sp['Date'] = pd.to_datetime(mn_sp.loc[:,'Date Local'], format='%Y-%m-%d')
sp_stats = mn_sp.groupby('Date')['Arithmetic Mean'].mean()
sns.relplot(data=sp_stats,
            label='Average µg/m³ of 2.5 micron\nparticles for the day')
plt.xticks(rotation=45, ha='right')
plt.axhline(y=12, color='g', label='Air quality is good below this')
plt.axhline(y=30, color='r', label='Air quality is bad above this')
plt.legend()
plt.title('Air quality in St. Paul')
plt.show()

# almost 10 years for Bakersfield
temp_df = pd.read_csv('daily_88101_2021.csv')
aq = pd.concat([aq, temp_df])
aq.duplicated().any()
aq.head()
print(aq.iloc[0])
for filename in ['daily_88101_2020.csv', 'daily_88101_2019.csv',
             'daily_88101_2018.csv', 'daily_88101_2017.csv',
             'daily_88101_2016.csv', 'daily_88101_2015.csv',
             'daily_88101_2014.csv', 'daily_88101_2013.csv',
             'daily_88101_2012.csv']:
    temp_df = pd.read_csv(filename)
    aq = pd.concat([aq, temp_df])
lt_bako = aq.loc[(aq['State Name'] == 'California') & \
    (aq['City Name'] == 'Bakersfield')]
lt_bako['Date'] = pd.to_datetime(lt_bako.loc[:,'Date Local'],
                                 format='%Y-%m-%d')
ltb = lt_bako.groupby('Date')['Arithmetic Mean'].mean()
sns.relplot(data=ltb, aspect=3,
            label='Average µg/m³ of 2.5 micron\nparticles for the day')
plt.xticks(rotation=45, ha='right')
plt.axhline(y=12, color='g', label='Air quality is good below this')
plt.axhline(y=30, color='r', label='Air quality is bad above this')
plt.legend()
plt.title('Air quality in Bakersfield 10y')
plt.show()

# four years including fires in San Jose
aq['Date'] = pd.to_datetime(aq.loc[:,'Date Local'], format='%Y-%m-%d')
start_date = pd.to_datetime('2019-01-01')
end_date = pd.to_datetime('2022-12-31')
sj_fires = aq.loc[(aq['State Name'] == 'California') & \
    (aq['City Name'] == 'San Jose') & (aq['Date'] >= start_date) & \
        (aq['Date'] <= end_date)]
sjf = sj_fires.groupby('Date')['Arithmetic Mean'].mean()
sns.relplot(data=sjf, aspect=2,
            label='Average µg/m³ of 2.5 micron\nparticles for the day')
plt.xticks(rotation=45, ha='right')
plt.axhline(y=12, color='g', label='Air quality is good below this')
plt.axhline(y=30, color='r', label='Air quality is bad above this')
plt.annotate('Fires', xy=(pd.to_datetime('2020-08-01'), 90), 
             xytext=(pd.to_datetime('2020-01-01'), 100),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.legend()
plt.title('Air quality for San Jose 2019 - 2022')
plt.show()