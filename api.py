import streamlit as st
import requests

response = requests.get('https://randomuser.me/api')
# print(response.status_code)
# print(response.json())

data = response.json()
gender = data["results"][0]["gender"].upper()
title = data["results"][0]["name"]["title"]
first_name = data["results"][0]["name"]["first"]
last_name = data["results"][0]["name"]["last"]
dob = data["results"][0]["dob"]["date"][:10]


# print(f'Name: {title}. {first_name} {last_name}')
# print(f'Gender: {gender}')
# print(f'DOB: {dob}')

random_person = f'{title}. {first_name} {last_name}'

st.write(f"""
# Today's Random person is...
*{random_person}*
\nGender: {gender}
\nBorn on: {dob}
""")
