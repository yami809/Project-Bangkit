import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style(style="whitegrid")
plt.style.use('fivethirtyeight')

to_month = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

to_year = {
    0: 2011,
    1: 2012
}

# hr_format = {
#     0: '12 am', 1: '1 am', 2: '2 am', 3: '3 am',
#     4: '4 am', 5: '5 am', 6: '6 am', 7: '7 am',
#     8: '8 am', 9: '9 am', 10: '10 am', 11: '11 am',
#     12: '12 pm', 13: '1 pm', 14: '2 pm', 15: '3 pm',
#     16: '4 pm', 17: '5 pm', 18: '6 pm', 19: '7 pm',
#     20: '8 pm', 21: '9 pm', 22: '10 pm', 23: '11 pm'
# }

season = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

def preprocess_data(df):
    df['mnth'] = df['mnth'].map(to_month)
    df['yr'] = df['yr'].map(to_year)
    # df['hr'] = df['hr'].map(hr_format)
    df['season'] = df['season'].map(season)
    return df

def filter_data(df, date_range, time_range=None):
    df_copy = df.copy()
    start_date, end_date = date_range
    df_copy['dteday'] = pd.to_datetime(df_copy['dteday'])

    df_copy = df_copy[df_copy['dteday'].dt.date >= start_date]
    if end_date is not None:
        df_copy = df_copy[df_copy['dteday'].dt.date <= end_date]

    if time_range is not None:
        df_copy = df_copy[df_copy['hr'] >= time_range[0].hour]
        df_copy = df_copy[df_copy['hr'] <= time_range[1].hour]

    return df_copy


def hourly_bar(df: pd.DataFrame, by='hr', col='cnt'):
    df_grouped = df.groupby(by).mean(numeric_only=True)[col]
    
    plot = sns.barplot(x=df_grouped.index, y=df_grouped)
    plot.set_xlabel(by)
    plot.set_ylabel("Average Count of Bike Rentals")
    
    return plot

def monthly_plot(df: pd.DataFrame, feature='cnt', return_df=False):
    df = df.copy()
    df.sort_values(['yr', 'mnth'], inplace=True)
    df['month'] = df['mnth'].map(to_month)
    df['year'] = df['yr'].map(to_year).astype(str)
    df['month_year'] = df['month'] + " " + df['year']

    df_feature_col = df.groupby('month_year')[feature].mean().reset_index()
    df_result = df_feature_col.set_index('month_year')

    if return_df:
        return df_result

    plt.figure(figsize=(12, 6))
    barplot = sns.barplot(x=feature, y='month_year', data=df_result, orient='h')
    barplot.set_title(f'Monthly Trend of Bike Rents by {feature}')
    barplot.set_xlabel(f'Average {feature.capitalize()} Count')
    barplot.set_ylabel('Month-Year')
    barplot.tick_params(axis='y', rotation=0)
    
    return barplot

def monthly_or_seasonly_pie(df: pd.DataFrame, by='season', col='cnt'):
    df_grouped = df.groupby(by).mean(numeric_only=True)[col]

    fig, ax = plt.subplots()
    ax.pie(df_grouped, labels=df_grouped.index, autopct='%.0f%%', startangle=90, counterclock=False)
    ax.set_title(f'{by} Trend of Bike Rentals')
    return fig
