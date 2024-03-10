import pandas as pd
import streamlit as st
import os
import datetime
from utils import *

dir = "./data/"
df_day = pd.read_csv(os.path.join(dir, "day.csv"))
df_hour = pd.read_csv(os.path.join(dir, "hour.csv"))

# Preproc
df_day = preprocess_data(df_day)
df_hour = preprocess_data(df_hour)

min_date = pd.to_datetime(df_day['dteday'].min())
max_date = pd.to_datetime(df_day['dteday'].max())

header, _ = st.columns([0.8, 0.2])

mode_col, date_col, time_start_col, time_end_col = header.columns([10, 15, 8, 8])

selected_mode = mode_col.radio("Select mode:", ["Daily", "Hourly"])

if selected_mode == "Daily":
    date_range = st.date_input(
        label='Select Date Range:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    df_cur = filter_data(df_day, date_range)
    
    monthly_plot = monthly_plot(df_cur)
    st.pyplot(monthly_plot.figure)

    column1, column2 = st.columns(2)

    seasonly_group_plot = monthly_or_seasonly_pie(df_cur, by='season')
    column1.pyplot(seasonly_group_plot)

    monthly_group_plot = monthly_or_seasonly_pie(df_cur, by='mnth')
    column2.pyplot(monthly_group_plot)


    # monthly_plot = monthly_plot(df_cur)
    # st.pyplot(monthly_plot.figure)

    # seasonly_group_plot = monthly_or_seasonly_pie(df_cur, by='season')
    # monthly_group_plot = monthly_or_seasonly_pie(df_cur, by='mnth')

    # st.pyplot(seasonly_group_plot, use_container_width=True)
    # st.pyplot(monthly_group_plot, use_container_width=True)

else:
    date_range = st.date_input(
        label='Select Date Range:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    time_start = st.time_input('Start Time:', datetime.time(0, 00))
    time_end = st.time_input('End Time:', datetime.time(23, 00))

    df_cur = filter_data(df_hour, date_range, (time_start, time_end))

    hourly_plot = hourly_bar(df_cur)
    st.pyplot(hourly_plot.figure)

    # seasonly_group_plot = monthly_or_seasonly_pie(df_cur, by='season')
    # monthly_group_plot = monthly_or_seasonly_pie(df_cur, by='mnth')

    # st.pyplot(seasonly_group_plot, use_container_width=True)
    # st.pyplot(monthly_group_plot, use_container_width=True)


    column1, column2 = st.columns(2)

    seasonly_group_plot = monthly_or_seasonly_pie(df_cur, by='season')
    column1.pyplot(seasonly_group_plot)

    monthly_group_plot = monthly_or_seasonly_pie(df_cur, by='mnth')
    column2.pyplot(monthly_group_plot)
    
st.dataframe(df_cur)
