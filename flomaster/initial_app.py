# import mysql.connector
# from mysql.connector import errorcode

import pandas as pd

import streamlit as st
import datetime
from time import perf_counter


import plotly.express as px


st.title("MVP for Automated report generation")

min_date = datetime.datetime(2015,1,1)
max_date = datetime.date(2023,11,18)

report_type = st.selectbox('Select the type of automated report',
                        ['Location', "Apporintment", 'Seen'])

merchant_id = st.number_input('Mechant id', min_value=1, max_value=10_000_000_000, value=7100000016, step=1)

start_date = st.date_input("Pick a start date", min_value=min_date, max_value=max_date)
end_date = st.date_input("Pick a end date", min_value=start_date, max_value=max_date)

print(f'Generating report for Merchant {merchant_id} from {start_date} to {end_date}')



db_config = {
            'user': 'zar.navasardyan',
            'password': 'London3030',
            'database': f'us2_qless',
            'host': f'dbreader.us2.int.qless.com',
            'use_unicode': True
        }

query = f"""select s.id 'Location Id', s.description Location, s.Enters 'Total Joined', s.Arrivals 'Total Arrived', (s.Enters - IFNULL(s.Arrivals,0)) 'Total No Shows' from 
            ( 
            select a.*, b.Arrivals, c.Summons from 
            (select ml.id, ml.description, count(distinct(sessionId)) Enters from EnterEvent ee 
            join Queue q on ee.queue_id = q.id 
            join MerchantLocation ml on q.location_id = ml.id 
            where ml.merchant_id = {merchant_id}  and 
                date between '{start_date}' and '{end_date}' and ml.deleted is not true 
            group by ml.id ) a 
        left join 
            (select ml.id, ml.description, count(distinct(sessionId)) Summons from TicketIssuedEvent tie 
            join Queue q on tie.queue_id = q.id 
            join MerchantLocation ml on q.location_id = ml.id 
            where ml.merchant_id = {merchant_id} and 
                date between '{start_date}' and '{end_date}' and ml.deleted is not true 
            group by ml.id ) c on a.id = c.id 
        left join 
            (select ml.id, ml.description, count(distinct(sessionId)) Arrivals from TicketRedeemedEvent tre 
            join Queue q on tre.queue_id = q.id 
            join MerchantLocation ml on q.location_id = ml.id 
            where ml.merchant_id = {merchant_id}  and
                date between '{start_date}' and '{end_date}' and ml.deleted is not true 
            group by ml.id ) b on a.id = b.id 
            ) s"""

query_with_groupby = f"""
        select  s.id 'Location Id', date_only_day,  s.description Location, s.Enters 'Total Joined', 
                s.Arrivals 'Total Arrived', (s.Enters - IFNULL(s.Arrivals,0)) 'Total No Shows' from
         (
        select a.*,  b.Arrivals,  c.Summons  from 
                
            (select ml.id, DATE(date) as date_only_day, ml.description, count(distinct(sessionId)) Enters from EnterEvent ee 
                     join Queue q on ee.queue_id = q.id 
                     join MerchantLocation ml on q.location_id = ml.id 
                     where ml.merchant_id = {merchant_id}  and 
                         date between '{start_date}' and '{end_date}' and ml.deleted is not true 
                     group by ml.id, date_only_day
         ) a
        left join 
                    (select ml.id, DATE(date) as date_only_day, ml.description, count(distinct(sessionId)) Summons from TicketIssuedEvent tie 
                    join Queue q on tie.queue_id = q.id 
                    join MerchantLocation ml on q.location_id = ml.id 
                    where ml.merchant_id = {merchant_id} and 
                        date between '{start_date}' and '{end_date}' and ml.deleted is not true 
                    group by ml.id, date_only_day) c on (a.id = c.id and a.date_only_day = c.date_only_day)
        left join 
                    (select ml.id, DATE(date) as date_only_day, ml.description, count(distinct(sessionId)) Arrivals from TicketRedeemedEvent tre 
                    join Queue q on tre.queue_id = q.id 
                    join MerchantLocation ml on q.location_id = ml.id 
                    where ml.merchant_id = {merchant_id} and 
                        date between '{start_date}' and '{end_date}' and ml.deleted is not true
                    group by ml.id, date_only_day )  b on (a.id = b.id and a.date_only_day = b.date_only_day)
                    ) s
                    """


cols_without_by_day = ['Location Id', 'Location', 'Total Joined', 'Total Arrived',  'Total No Shows']
cols_with_by_day = ['Location Id', "Date", 'Location', 'Total Joined', 'Total Arrived',  'Total No Shows']



def get_df(query, columns, db_config):
    return pd.read_csv('loc.csv')
    # conn = mysql.connector.connect(**db_config)
    # cursor = conn.cursor()



    # cursor.execute(query)
    # results = cursor.fetchall()

    # if results == []:
    #     return 'No data fetched, check your input'
    # else:
    #     results_df = pd.DataFrame(results, columns=columns)
    #     return results_df




st.markdown("## Data Fetched")
start_time = perf_counter()
df = get_df(query_with_groupby, cols_with_by_day, db_config)
print(df)
st.write(df)
df.to_csv('loc.csv', index=False)
print(f'fetched data in {perf_counter() - start_time}')

location = st.selectbox('Select a location to see detailed view',
                        df['Location'].unique())

print(location)

start_time = perf_counter()
df_by_day = get_df(query_with_groupby, cols_with_by_day, db_config)
df_for_loc = df_by_day[df_by_day['Location'] == location]

st.write(df_for_loc)
print(f'fetched data in {perf_counter() - start_time}')



def get_report_for_df(df):
    # df = df.rename(columns={'date':'index'}).set_index('index')#[['index', 'Total Joined']]
    # return df

    fig = px.line(df, x='Date', y=['Total Joined', 'Total Arrived',  'Total No Shows'], markers=True)
    return fig
    # return st.line_chart(df.rename(columns={'date':'index'}).set_index('index')[['index', 'Total Joined']])


fig = get_report_for_df(df_for_loc)
st.plotly_chart(fig)