import streamlit as st
import pandas as pd
import numpy as np

@st.cache
def load_data():
    cases_url = 'https://healthdata.gov/resource/di4u-7yu6.csv?$limit=5000'
    cases_df = pd.read_csv(cases_url)

    date_to_use = cases_df.groupby('date').size().head().reset_index().loc[0,'date']
    vaccine_url = f'https://data.cdc.gov/resource/8xkx-amqh.csv?$limit=5000&date={date_to_use}'
    vaccine_df = pd.read_csv(vaccine_url)

    vaccine_df['fips'] = vaccine_df['fips'].replace({'UNK':np.nan})
    vaccine_df = vaccine_df.dropna(subset=['fips'])
    vaccine_df['fips'] = vaccine_df['fips'].astype('int')

    cases_cols = ['fips','county','state','cases_last_7_days','cases_per_100k_last_7_days']
    vaccine_cols = ['fips','recip_county','recip_state','series_complete_pop_pct',
                    'series_complete_18plus','series_complete_18pluspop','completeness_pct']
    merged = cases_df[cases_cols].merge(vaccine_df[vaccine_cols],
                                        on='fips')
    merged = merged.sort_values(['recip_state','recip_county'])
    
    return merged
st.write('# Local CDC Covid Data')
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Data downloaded from CDC")
st.write('https://healthdata.gov/dataset/COVID-19-Community-Profile-Report-County-Level/di4u-7yu6 and https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh')

state_list = data['recip_state'].unique().tolist()
state = st.selectbox('State', state_list)

county_list = data[data['recip_state'] == state]['recip_county'].unique()
county = st.selectbox('County', county_list)

filtered = data[(data['recip_state'] == state) & (data['recip_county'] == county)].head(1).to_dict(orient='records')
st.write(filtered)