import streamlit as st
import SessionState
import pandas as pd
import numpy as np
import math
import base64
from io import BytesIO
from scipy import stats

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

    st.markdown("This web application calculates the estimated probability of infection in an indoor environment based on several factors.")
    st.markdown("<< You can adjust these factors in the Parameters panel to the left.")
    
    with st.beta_expander(label='Detailed Instructions', expanded=False):
        with open('instructions.md', 'r') as instructions_md:
            instructions_text = instructions_md.read()
            st.markdown(instructions_text)
    with st.beta_expander(label='Sample scenarios'):
        with open('scenarios.md','r') as scenarios_md:
            scenarios_text = scenarios_md.read()
            st.markdown(scenarios_text)            
    with st.beta_expander(label='Explanation of how this works'):
        st.markdown('Based on version 3.4.22 of [https://tinyurl.com/covid-estimator](https://tinyurl.com/covid-estimator)')
        with open('explanation.md','r') as explanation_md:
            explanation_text = explanation_md.read()
            st.markdown(explanation_text)
    st.sidebar.markdown('# Parameters')
    option = st.sidebar.selectbox('Presets',
                                 ('OCIO Video Conference Room, CapGal 4001 ', 'Freer Staff Library, G203', 'Break Room SMS, 118', 'Small exhibit gallery, Hirshhorn 202', 'Outer Ring Corridor, Hirshhorn 4th floor', 'Break Room, MSC, G2002B', 'LAB Processing Lab, MSC D1015', 'Classroom, NASM Udvar-Hazy 101.06B', 'Mary Baker Engen Restoration Hanger, NASM Udvar-Hazy 113.03', 'Family History Center, NMAAHC 2052', 'Health Services, NMAAHC C3050', 'Museum Shop, NMAAHC 1025', 'S C Johnson Conference Room A, NMAH 1014', 'Collections Workroom, NMAI LL-2144', 'Conservation Scientific Lab, NMAI E-3099', 'Anthropology  Library, NMNH 330', 'Fossil prep lab NMNH 25', 'LAB Break Room, NMNH W107', 'Education Center Classroom, QUAD 3037', 'Reptile Discovery Center, NZP F100A),
                                 help='Tooltip')
    preset_dict = {'OCIO Video Conference Room, CapGal 4001':{'length':26.7,
                           'width':26.7,
                           'area':714,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Freer Staff Library, G203':{'length':23.1,
                           'width':23.1,
                           'area':535,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Break Room, SMS 118':{'length':12.2,
                           'width':12.2,
                           'area':149,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Small exhibit gallery, Hirshhorn 202':{'length':18.6,
                           'width':18.6,
                           'area':347,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Outer Ring Corridor, Hirshhorn 4th floor':{'length':41.8,
                           'width':41.8,
                           'area':1747,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Break Room, MSC, G2002B':{'length':17.7,
                           'width':17.7,
                           'area':313,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'LAB Processing Lab, MSC D1015':{'length':41.2,
                           'width':41.2,
                           'area':1699,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Classroom, NASM Udvar-Hazy 101.06B':{'length':34.9,
                           'width':34.9,
                           'area':1215,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Mary Baker Engen Restoration Hanger, NASM Udvar-Hazy 113.03':{'length':144.9,
                           'width':144.9,
                           'area':20998,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Family History Center, NMAAHC 2052':{'length':41.5,
                           'width':41.5,
                           'area':1719,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Health Services, NMAAHC C3050':{'length':12.5,
                           'width':12.5,
                           'area':157,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Museum Shop, NMAAHC 1025':{'length':49.5,
                           'width':49.5,
                           'area':2454,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'S C Johnson Conference Room A, NMAH 1014':{'length':30.6,
                           'width':30.6,
                           'area':936,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Collections Workroom, NMAI LL-2144':{'length':40.2,
                           'width':40.2,
                           'area':1618,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Conservation Scientific Lab, NMAI E-3099':{'length':18.4,
                           'width':18.4,
                           'area':339,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Anthropology Library, NMNH 330':{'length':43.0,
                           'width':43.0,
                           'area':1852,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Fossil Prep Lab NMNH 25':{'length':36.3,
                           'width':36.3,
                           'area':1320,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'LAB Break Room, NMNH W107':{'length':13.7,
                           'width':13.7,
                           'area':189,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Education Center Classroom, QUAD 3037':{'length':40.4,
                           'width':40.4,
                           'area':1636,
                           'height':10,
                           'ach':6,
                           'merv':13},
               'Reptile Discovery Center, NZP F100A':{'length':25.5,
                           'width':25.5,
                           'area':648,
                           'height':10,
                           'ach':6,
                           'merv':13}
                }
    st.sidebar.markdown('### Room measurements')

    b15 = st.sidebar.number_input('Floor area of room (in ft²)', value=preset_dict[option]['area'])
    #b14 = st.sidebar.number_input('Width of room (in ft)', value=preset_dict[option]['width'])
    b16 = st.sidebar.number_input('Height of room (in ft)', value=preset_dict[option]['height'])
    
    ### Calculating room volume
#    e13 = b13 * 0.305
#    e14 = b14 * 0.305
#    e15 = e13 * e14
    e15 = b15 / 10.764
    e16 = b16 * 0.305
#    e17 = e13 * e14 * e16
    e17 = e15 * e16
    
    ach_dict = {'Closed Windows (0.3)':0.3,
                'Open Windows (2.0)': 2.0,
                'Mechanical Ventilation (3.0)': 3.0,
                'Smithsonian Standard (6.0)': 6.0,
                'Better mechanical ventilation (8.0)': 8.0,
                'Laboratory, Restaurant (9.0)': 9.0,
                'Bar (15.0)': 15.0,
                'Hospital/Subway Car (18.0)': 18.0,
                'Airplane (24.0)': 24.0}
    ach_select = st.sidebar.selectbox('Air changes per hour', 
                               list(ach_dict.keys()),
                               index=preset_dict[option]['ach'])
    b28 = ach_dict[ach_select]
    merv_dict = {'MERV 0 (None)':0,
                 'MERV 2 (Res. Window AC)': 2,
                 'MERV 6 (Res./Comm./Industrial)': 6,
                 'MERV 10 (Res./Comm./Hospital)': 10,
                 'MERV 13 (Smithsonian Standard)': 13,
                 'MERV 14 (Hospital & General Surgery)': 14,
                 'MERV 17 (HEPA)': 17}
    merv_select = st.sidebar.selectbox(
                'Filtration System',
                options=list(merv_dict.keys()),
                index=preset_dict[option]['merv'])
    merv_value = merv_dict[merv_select]
    
    recirc_dict = {'None (0)':0,
                'Slow (0.3)': 0.3,
                'Moderate (1.0)': 1.0,
                'Fast (10.0)': 10.0,
                'Airplane (24.0)': 24.0,
                'Subway Car (54.0)': 54.0}
    recirc_select = st.sidebar.selectbox('Recirculation Rate (per hour)', 
                               list(recirc_dict.keys()),
                               index=2)
    recirc_rate = recirc_dict[recirc_select]
    
    st.sidebar.markdown('### Advanced parameters')
    breathing_dict = {'Resting (0.49)': 0.49,
                      'Standing (0.54)': 0.54,
                      'Singing (1.00)': 1.00,
                      'Light Exercise (1.38)': 1.38,
                      'Moderate Exercise (2.35)': 2.35,
                      'Heavy Exercise (3.30)': 3.30}
    breathing_select = st.sidebar.selectbox('Breathing rate of susceptibles (m³/hr)', 
                               list(breathing_dict.keys()),
                               index=0)
    b47 = breathing_dict[breathing_select]
    #b47 = st.sidebar.number_input('Breathing rate of susceptibles (m3/hr)', value=0.72)
    resp_dict = {'Breathing (light) (1.1)': 1.10,
                 'Breathing (normal) (4.2)': 4.20,
                 'Breathing (heavy) (8.8)': 8.80,
                 'Talking (whisper) (29.0)': 29.00,
                 'Talking (normal) (72.0)': 72.00,
                 'Talking (loud) (142.0)': 142.00,
                 'Singing (970.0)': 970.0}
    resp_select = st.sidebar.selectbox('Respiratory Activity: (q/m³)', 
                               list(resp_dict.keys()),
                               index=0)   
    b51 = resp_dict[resp_select] * b47

    st.sidebar.markdown('q/h ='+'{:.2f}'.format(b51))

    b53 = st.sidebar.slider('Mask fit/compliance', 0, 100, value = 100)
    mask_ex_dict = {'None (0%)': 0.0,
                'Face shield (23%)': 23,
                'Cloth mask (50%)': 50.0,
                'Disposable surgical (65%)': 65.0,
                'N95, KN95 masks (90%)': 90.0}
    mask_ex_select = st.sidebar.selectbox(
            'Mask efficiency',
            options=list(mask_ex_dict.keys()),
            index=3)
    b52 = mask_ex_dict[mask_ex_select]
    b54 = b52
    #b52 = st.sidebar.number_input('Exhalation mask efficiency (%)', value=50)
    #b54 = st.sidebar.number_input('Inhalation mask efficiency', value=30)

    st.sidebar.markdown('### Scenario parameters')
    b24 = st.sidebar.number_input('Duration of event (in min)', value=480)
    si_cap = math.floor((b15) / 113)
    six_foot_cap = math.floor((b15) / 36)
    st.sidebar.markdown(f'*SI recommendations of 113 ft² per person would accomodate **{si_cap}** people in this space.*')
    b38 = st.sidebar.number_input('Total number of people present', value=12)
    b39 = st.sidebar.number_input('Infective people', value=1)
    immune = st.sidebar.number_input('Immune people', value=1)
    suscept = b38 - immune - b39

    ## Calculations


    e24 = b24/60

    ### Calculation aerosol filtration
    # Source: https://www.ashrae.org/technical-resources/filtration-disinfection
    # Table of MERV values corresponding to aerosol filtration efficiency, by different particle sizes (in microns)
    merv_eff_dict = [
        {'merv': 0, '0.3-1': 0, '1-3': 0, '3-10': 0},
        {'merv': 1, '0.3-1': 0.01, '1-3': 0.01, '3-10': 0.01},
        {'merv': 2, '0.3-1': 0.01, '1-3': 0.01, '3-10': 0.01},
        {'merv': 3, '0.3-1': 0.01, '1-3': 0.01, '3-10': 0.01},
        {'merv': 4, '0.3-1': 0.01, '1-3': 0.01, '3-10': 0.01},
        {'merv': 5, '0.3-1': 0.01, '1-3': 0.01, '3-10': 0.2},
        {'merv': 6, '0.3-1': 0.01, '1-3': 0.01, '3-10': 0.35},
        {'merv': 7, '0.3-1': 0.01, '1-3': 0.01, '3-10': 0.50},
        {'merv': 8, '0.3-1': 0.01, '1-3': 0.20, '3-10': 0.70},
        {'merv': 9, '0.3-1': 0.01, '1-3': 0.35, '3-10': 0.75},
        {'merv': 10, '0.3-1': 0.01, '1-3': 0.50, '3-10': 0.80},
        {'merv': 11, '0.3-1': 0.2, '1-3': 0.65, '3-10': 0.85},
        {'merv': 12, '0.3-1': 0.35, '1-3': 0.80, '3-10': 0.90},
        {'merv': 13, '0.3-1': 0.50, '1-3': 0.85, '3-10': 0.90},
        {'merv': 14, '0.3-1': 0.75, '1-3': 0.90, '3-10': 0.95},
        {'merv': 15, '0.3-1': 0.85, '1-3': 0.90, '3-10': 0.95},
        {'merv': 16, '0.3-1': 0.95, '1-3': 0.95, '3-10': 0.95},
        {'merv': 17, '0.3-1': 0.9997, '1-3': 0.9997, '3-10': 0.9997},
        {'merv': 18, '0.3-1': 0.99997, '1-3': 0.99997, '3-10': 0.99997},
        {'merv': 19, '0.3-1': 0.999997, '1-3': 0.999997, '3-10': 0.999997},
        {'merv': 20, '0.3-1': 0.9999997, '1-3': 0.9999997, '3-10': 0.9999997},
    ]
    aerosol_radius = 2
    for item in merv_eff_dict:
        if item['merv'] == merv_value:
            if aerosol_radius < 1:
                eff = item['0.3-1']
            elif aerosol_radius < 3:
                eff = item['1-3']
            else:
                eff = item['3-10']

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
    indiv_prob_formatted = '{:.2f}%'.format(b71)
    at_least_one_prob = 1 - stats.binom.cdf(0, suscept, b71)
    at_least_one_formatted = '{:.2f}%'.format(at_least_one_prob)
    
    st.markdown('## Overall Results')
    st.markdown('*This result will update live as you change parameters in the sidebar.*')

    st.markdown(f'Each susceptible individual has **{indiv_prob_formatted}** probability of getting infected')
    st.markdown(f'With **{suscept}** susceptible individuals, there is a  **{at_least_one_formatted}** probability that at least one person will get infected')
    #b26 = st.number_input('Number of repetitions of event', value=26)
    #st.write(f'Probability of infection over {b26} repetitions:')


#    st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .footer{padding: 10px 16px; background: #555; color: #f1f1f1; position:fixed;bottom:0;} .sticky { position: fixed; bottom: 0; width: 100%;} </style><div class="footer sticky" id="sticky-footer"><i>Based on input parameters,</i><br/>Probability of infection: '+prob_formatted+'</div>', unsafe_allow_html=True)

#    with st.beta_expander(label='Intermediate Calculations'):
#        st.write(f'First order loss rate: {b32} h-1')
#        st.write(f'Ventilation rate per person: {b34} L/s/person')

    io_df = pd.DataFrame([{'Room Area (sq. ft)':b15,
                         'Room Height (ft)':b16,
                         'Probability of Infection (%)': b71}])
    st.table(io_df)

    save_button = st.button('Add scenario to table')

    saved_df = pd.DataFrame(columns=['Room Length (ft)','Room Width (ft)','Probability of Infection (%)'])
    state = SessionState.get(saved_df = pd.DataFrame(columns=['Room Length (ft)','Room Width (ft)','Probability of Infection (%)']))
    if save_button:
        state.saved_df = state.saved_df.append(io_df, ignore_index=True)
    st.dataframe(state.saved_df)
    st.markdown(get_table_download_link(state.saved_df), unsafe_allow_html=True)    
    
    with open('footer.md', 'r') as footer_md:
        footer_text = footer_md.read()
        st.markdown(footer_text)

if __name__ == "__main__":
    main()
