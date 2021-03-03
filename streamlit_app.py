import streamlit as st
import SessionState
import pandas as pd
import numpy as np
import math
import base64
from io import BytesIO

def to_excel(df):
    #From https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/12
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="scenarios.xlsx">Download Excel file</a>' 


def main():
    st.title('Covid-19 Aerosol Transmission Estimator')
    st.markdown('Based on version 3.4.22 of [https://tinyurl.com/covid-estimator](https://tinyurl.com/covid-estimator)')
    with st.beta_expander(label='Instructions', expanded=True):
        st.markdown('*Detailed instructions here*')
    with st.beta_expander(label='Explanation of how this works'):
        st.markdown('*Lots of links to additional sources, etc.*')
    st.sidebar.markdown('# Parameters')
    option = st.sidebar.selectbox('Presets',
                                 ('Rotunda', 'Office', 'Lab'))
    preset_dict = {'Rotunda':{'length':250,
                              'ach':4},
                    'Office':{'length':25,
                              'ach':2},
                    'Lab':{'length':100,
                              'ach':1}}
    st.sidebar.markdown('### Room measurements')
    b13 = st.sidebar.number_input('Length of room (in ft)', value=preset_dict[option]['length'])
    b14 = st.sidebar.number_input('Width of room (in ft)', value=20)
    b16 = st.sidebar.number_input('Height of room (in ft)', value=10)
    ach_dict = {'Closed Windows (0.3)':0.3,
                'Open Windows (2.0)': 2.0,
                'Mechanical Ventilation (3.0)': 3.0,
                'Open windows with fans (6.0)': 6.0,
                'Better mechanical ventilation (8.0)': 8.0,
                'Laboratory, Restaurant (9.0)': 9.0,
                'Bar (15.0)': 15.0,
                'Hospital/Subway Car (18.0)': 18.0,
                'Airplane (24.0)': 24.0}
    ach_select = st.sidebar.selectbox('Air changes per hour', 
                               list(ach_dict.keys()),
                               index=preset_dict[option]['ach'])
    b28 = 3
    b28 = ach_dict[ach_select]
    merv_dict = {'None':0,
                 'MERV 2': 2,
                 'MERV 6': 6,
                 'MERV 17': 17}
    merv_select = st.sidebar.select_slider(
                'Filtration System',
                options=list(merv_dict.keys()),
                value='MERV 6')
    recirc_dict = {'None (0)':0,
                'Slow (0.3)': 0.3,
                'Moderate (1.0)': 1.0,
                'Fast (10.0)': 10.0,
                'Airplane (24.0)': 24.0,
                'Subway Car (54.0)': 54.0}
    recirc_select = st.sidebar.selectbox('Recirculation Rate (per hour)', 
                               list(recirc_dict.keys()),
                               index=2)
    
    st.sidebar.markdown('### Advanced parameters')
    b47 = st.sidebar.number_input('Breathing rate of susceptibles (m3/hr)', value=0.72)
    b51 = st.sidebar.number_input('Quanta exhalation rate of infected (quanta/hr)', value=10)
    b52 = st.sidebar.number_input('Exhalation mask efficiency (%)', value=50)
 #   b53 = st.sidebar.number_input('Fraction of people w/ masks', value=100)
    b53 = st.sidebar.slider('Percentage of people w/ masks', 0, 100, value = 100)
    b54 = st.sidebar.number_input('Inhalation mask efficiency', value=30)

    st.sidebar.markdown('### Scenario parameters')
    b24 = st.sidebar.number_input('Duration of event (in min)', value=480)
    b26 = st.sidebar.number_input('Number of repetitions of event', value=26)
    b38 = st.sidebar.number_input('Total number of people present', value=12)
    b39 = st.sidebar.number_input('Infective people', value=1)

    ## Calculations
    ### Calculating room volume
    e13 = b13 * 0.305
    e14 = b14 * 0.305
    e15 = e13 * e14
    e16 = b16 * 0.305
    e17 = e13 * e14 * e16

    e24 = b24/60

    ### Calculating first order loss rate
    b29 = 0.62
    b30 = 0.3
    b31 = 0
    b32 = b28 + b29 + b30 + b31

    ### Calculating ventilation rate per person
    b34 = e17 * (b28 + b31) * 1000 / 3600 / b38

    ### Calculating quanta
    b66 = b51 * (1 - (b52/100) * (b53/100)) * b39
    b67 = b66/b32/e17 * (1-(1/b32/e24) * (1 - math.exp(-1 * b32 * e24)))
    b68 = b67 * b47 * e24 * (1 - (b54/100) * (b53/100))

    b71 = (1 - math.exp(-1 * b68)) * 100

    st.markdown('### Overall Results')
    st.write(f'Probability of infection in a single event: {b71}%')
    st.write(f'Probability of infection over {b26} repetitions:')

    with st.beta_expander(label='Intermediate Calculations'):
        st.write(f'First order loss rate: {b32} h-1')
        st.write(f'Ventilation rate per person: {b34} L/s/person')

    io_df = pd.DataFrame([{'Room Length (ft)':b13,
                         'Room Width (ft)':b14,
                         'Probability of Infection (%)': b71}])
    st.table(io_df)

    save_button = st.button('Add scenario to table')

    saved_df = pd.DataFrame(columns=['Room Length (ft)','Room Width (ft)','Probability of Infection (%)'])
    state = SessionState.get(saved_df = pd.DataFrame(columns=['Room Length (ft)','Room Width (ft)','Probability of Infection (%)']))
    if save_button:
        state.saved_df = state.saved_df.append(io_df, ignore_index=True)
    st.dataframe(state.saved_df)
    st.markdown(get_table_download_link(state.saved_df), unsafe_allow_html=True)    

    st.markdown('*Lots of additional disclaimers down here*')

if __name__ == "__main__":
    main()