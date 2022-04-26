import pyrebase
import streamlit as st
import pandas as pd
from google.cloud import firestore
from st_aggrid import AgGrid
import requests
import json


st.title('CryptoScamDB')
st.image('https://time.com/nextadvisor/wp-content/uploads/2021/11/Common-crypto-scams-to-watch-out-for-884x584.jpg')

# Configuration Key
firebaseConfig = {
  'apiKey': "AIzaSyAs7s4nBspSeIeekJmoq-rMhE9in_9xsiM",
  'authDomain': "testprojectdsci551.firebaseapp.com",
  'databaseURL': "https://testprojectdsci551-default-rtdb.firebaseio.com",
  'projectId': "testprojectdsci551",
  'databaseURL': "https://testprojectdsci551-default-rtdb.firebaseio.com/",
  'storageBucket': "testprojectdsci551.appspot.com",
  'messagingSenderId': "680668884953",
  'appId': "1:680668884953:web:5dd68fcaa35ca9f9d133c8",
  'measurementId': "G-445KRB68VT"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

st.sidebar.title("Crypto Scam DB")

# Authentication

choice = st.sidebar. selectbox('Login/Signup', ['Login', 'Sign up'])

email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password',type = 'password')

if choice == 'Sign up':
    handle = st.sidebar.text_input('Please input a user name')
    submit = st.sidebar.button('Create my account')

    if submit:
        user = auth.create_user_with_email_and_password(email,password)
        st.success('Your account is created sucessfully!')
        # Sign in
        user = auth.sign_in_with_email_and_password(email,password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome ' + handle)
        st.info('Login via login drop down selection')

elif choice == 'Login':
    submit = st.sidebar.button('Login')
    if submit:
        user = auth.sign_in_with_email_and_password(email,password)
        qry = db.child(user['localId']).child("Handle").get()
        handle = qry.val()
        st.title('Welcome ' + handle)
        st.info('Login via login drop down selection')

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
bio = st.radio('Jump to',['Home','Search for Scams', 'Report Scams'])

# Display general stats and info tab code
if bio == 'Home':
    header = st.container()
    dataset = st.container()
    tables = st.container()
    questions = st.container()

    with header:
        st.title('Welcome!')
        st.text('Know of a crypto scam? Please report below to protect your fellow investors!')

    with tables:
        st.header('Scam Watch')
        # st.text('Take a look at scams that we are aware of: ')
        @st.cache
        def data_upload():
            df = pd.read_json('https://testprojectdsci551-default-rtdb.firebaseio.com/__collections__/scams/.json')
            return df

        df = data_upload()
        # st.dataframe(data=df)

        AgGrid(df)

        # st.text('\n')
        num_scams = len(df)
        st.text('There are currently ' + str(num_scams) + ' scams reported to CryptoScamDB.')


# Report scams tab code
elif bio == 'Report Scams':
    header = st.container()
    questions = st.container()
    tables = st.container()
    questions = st.container()
    with header:
        st.title('Report Scams')

    with questions:
        st.subheader('List any of the details below about the scam: ')

        input_q1 = st.text_input('Scam Name')
        input_q2 = st.text_input('Website url')
        input_q3 = st.text_input('Coin Ticker ID')
        input_q4 = st.text_input('Address')
        input_q5 = st.text_input('Description')

        if st.button('Submit'):
            #qry = db.child(user['localId']).child("Handle").get()
            #handle = qry.val()
            data = {"name": input_q1, "url": input_q2, "coin": input_q3, "addresses": [input_q4], "description": input_q5}
            db.child("__collections__").child("scams").push(data)
            st.write('Your scam report was submitted sucessfully! Thank you!')

 


# Search for scams tab code
elif bio == 'Search for Scams':
    header = st.container()
    questions = st.container()
    tables = st.container()
    questions = st.container()
    with header:
        st.title('Scam Query')
    #with questions:
        #st.subheader('Search Criteria:')
    drop = st.selectbox('Search for scams based on wallet address or website URL:', options=['Wallet Address', 'Website'])
    search_text = st.text_input('Enter text to search:')
    if st.button('Submit'):
        # Code for searching a wallet address
        if drop == 'Wallet Address':
            #Check the Bitcoin Abuse API and list results in text
            #The token is my api key
            token = 'ufF3UhDMfEK0Rv8FLJnX9H0JSWQAF6SXVLNYHJaJTfT1fagEcWWx4JpuS78U'
            r = requests.get("https://www.bitcoinabuse.com/api/reports/check?address="+search_text+"&api_token="+token)
            count = r.json()['count']
            if count > 0:
                st.write('--BTC Abuse Record Check--')
                st.write('Report Count: ' + str(count))
                abusetype = r.json()['recent'][0]['abuse_type_id']
                a = requests.get("https://www.bitcoinabuse.com/api/abuse-types")
                for item in a.json():
                    if item['id'] == int(abusetype):
                        print('Abuse type: ' + item['label'])
                desc = r.json()['recent'][0]['description']
                st.write("Last Report Comment: " + str(desc))
                st.write('See all report record details here:')
                st.write('https://www.bitcoinabuse.com/reports/' + str(search_text))

        # Check database and output to dataframe
            mylist = []
            qry = db.child("__collections__").child("scams").get()
            for item in qry:
                mylist.append(item.val())
            for item in mylist:
                try:
                    if "addresses" in item:
                        for address in item['addresses']:
                            if address == search_text:
                                results = db.child("__collections__").child("scams").order_by_child("id").equal_to(item['id']).get()
                                for result in results:
                                    df = pd.DataFrame.from_dict(result.val())
                except:
                    pass

            with tables:
                try:
                    @st.cache
                    def data_upload():
                        #df = pd.DataFrame.from_dict(results.val())
                        return df

                    df = data_upload()

                    AgGrid(df)
                except:
                    pass

        # Code for searching a website
        if drop == 'Website':
            try:
                qry = db.child("__collections__").child("scams").order_by_child("url").equal_to(search_text).get()
                mylist = []
                for result in qry:
                    mylist.append(result.val())
                    mylist[0]['f'] = [1]
                    df = pd.DataFrame.from_dict(mylist[0])

            except:
                pass

            with tables:
                try:
                    @st.cache
                    def data_upload():
                        #df = pd.DataFrame.from_dict(results.val())
                        return df

                    df = data_upload()

                    AgGrid(df)
                except:
                    pass
