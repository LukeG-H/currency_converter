import streamlit as st
import requests

# get some data from api and cache it:
# @st.cache_data
def get_data():
    response = requests.get('https://randomuser.me/api')
    # print(response.status_code)
    # print(response.json())
    return response

# convert response into raw json data:
data = get_data().json()

# format selected data (should be a function but this is fine for now):
gender = data["results"][0]["gender"].upper()
title = data["results"][0]["name"]["title"]
first_name = data["results"][0]["name"]["first"]
last_name = data["results"][0]["name"]["last"]
dob = data["results"][0]["dob"]["date"][:10]
age = data["results"][0]["dob"]["age"]

random_person = f'{title}. {first_name} {last_name}'

# display data using streamlit:
st.write(f"""
# Today's Random person is...
*{random_person}*
\nGender: {gender}
\nAge: {age}
\nBorn on: {dob}
""")


slider = st.slider("This is their age on a slider!", 0, 100, age)
calendar = st.date_input("Birthday",dob)
