import streamlit as st
import requests
from typing import Union

# get some data from API and cache it
# early return if API call is not successful
# added test_status to test error conditions
# @st.cache_data (turned off for testing)
def get_data(test_status: int = None) -> Union[dict, str]:
    response = requests.get('https://randomuser.me/api')
    status = test_status if test_status is not None else response.status_code

    if status != 200:
        status_message: str = f"Status: {status}\nOops... something went wrong!"
        return status_message

    data = response.json()
    return data


# format selected data and return a new 'person' dict.
# use try except raise for handling errors if the data structure changes
def format_data(data: dict) -> dict:
    try:
        result: str = data["results"][0]
        title: str = result["name"]["title"]
        first_name: str = result["name"]["first"]
        last_name: str = result["name"]["last"]
        full_name: str = f"{title}. {first_name} {last_name}"

        return {
            "name": full_name,
            "gender": result["gender"].upper(),
            "dob": result["dob"]["date"][:10],
            "age": result["dob"]["age"]
        }
    except (KeyError, IndexError) as err:
        raise ValueError("Unexpected data format") from err


# display data using streamlit:
def display(person: dict) -> None:
    st.write(f"""
    # Today's Random person is...
    \n*{person["name"]}*
    \nGender: {person["gender"]}
    \nAge: {person["age"]}
    \nBorn on: {person["dob"]}
    """)
    
    slider: int  = st.slider("This is their age on a slider!", 0, 100, person["age"])
    calendar: str = st.date_input("Birthday:", person["dob"])


def main() -> None:
    person_data: dict = get_data()

    if isinstance(person_data, str):
        st.error(person_data)
        st.error("Failed to fetch data. Please check your internet connection or try again later.")
        return

    person: dict = format_data(person_data)
    display(person)


if __name__ == '__main__':
    main()