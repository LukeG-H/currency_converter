import streamlit as st
import requests

# get some data from api:
response = requests.get('https://randomuser.me/api')
# print(response.status_code)
# print(response.json())

# format selected data (should be a function but this is fine for now):
data = response.json()
gender = data["results"][0]["gender"].upper()
title = data["results"][0]["name"]["title"]
first_name = data["results"][0]["name"]["first"]
last_name = data["results"][0]["name"]["last"]
dob = data["results"][0]["dob"]["date"][:10]

random_person = f'{title}. {first_name} {last_name}'

# display data using streamlit:
st.write(f"""
# Today's Random person is...
*{random_person}*
\nGender: {gender}
\nBorn on: {dob}
""")
