'encoding=utf-8'

import streamlit as st
import pandas as pd

header = st.container()
dataset = st.container()
tables = st.container()
questions = st.container()

with header:
    st.title('CryptoScamDB')
    st.text('Know of a scam? Please report below to protect your fellow investors!')

with tables:
    st.header('Scam Watch')
    st.text('Take a look at scams we have aggregated in our database: ')

# take df from scams.py
    data = pd.read_csv('scams.csv', index_col=False)
    st.write(data)

    # num_scams = pd.DataFrame(data['URL'].value_counts())
    # print(num_scams)
    # st.text('There are currently ' + num_scams + ' scams reported to CryptoScamDB.')

# show df too, make columns visible, maybe agg by coin or something??

with questions:
    st.subheader('Tell us more here: ')

drop = st.selectbox('How many years have you been in crypto?', options=['Select one', '<1', '1-3', '3-5', '6+'])
input_q1 = st.text_input('Which coins were targeted in this scam?')
input_q2 = st.text_input('What amount of those coins were targeted in this scam?')
input_q3 = st.text_input('Which wallet do you use to store your coins?')
input_q4 = st.text_input('Please provide a description below.')


# URLs to crypto scam alrts like whale alert or scam alert, etc?
