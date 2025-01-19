import streamlit as st
import requests

# get some data from api and cache it (turned off for testing):
# @st.cache_data
def get_data() -> requests.Response:
    response = requests.get('https://randomuser.me/api')
    return response

# format selected data:
def format_data(data: dict) -> dict:
    person: dict = {}

    title: str = data["results"][0]["name"]["title"]
    first_name: str = data["results"][0]["name"]["first"]
    last_name: str = data["results"][0]["name"]["last"]
    full_name: str = f'{title}. {first_name} {last_name}'
    
    person["name"] = full_name
    person["gender"] = data["results"][0]["gender"].upper()
    person["dob"] = data["results"][0]["dob"]["date"][:10]
    person["age"] = data["results"][0]["dob"]["age"]

    return person

# display data using streamlit:
def display(person: dict) -> None:
    st.write(f"""
    # Today's Random person is...
    \n*{person["name"]}*
    \nGender: {person["gender"]}
    \nAge: {person["age"]}
    \nBorn on: {person["dob"]}
    """)
    
    slider = st.slider("This is their age on a slider!", 0, 100, person["age"])
    calendar = st.date_input("Birthday:", person["dob"])


def main() -> None:
    person_data: dict = get_data().json()
    person: dict = format_data(person_data)
    display(person)


if __name__ == '__main__':
    main()