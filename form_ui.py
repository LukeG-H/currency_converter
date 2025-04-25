import streamlit as st
import time
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from currencies import CURRENCY_OPTIONS
from typing import *


class FormUi:
    def __init__(self):
        self.title()
        self.form_values: Dict[str, str | float | None] = {
            "from_currency": None,
            "to_currency": None,
            "amount": None
            }
        # self.conversion_form()

    def title(self) -> None:
        """Sets the page title (header)"""
        # st.title("""
        # Currency Converter\n*Currency data updated hourly*
        # """)
        self.title = colored_header(
            label="Currency Converter",
            description="*Currency data updated hourly*",
            color_name="violet-70",
        )

    def annimation(self):
        """Annimation displayed on Submission of the form"""
        rain(
            emoji = "💱",
            font_size = 60,
            falling_speed = 2,
            animation_length = 1,
        )

    # Conversion form for user inputs
    def conversion_form(self) -> Dict[str, str | float] | None:
        """Main currency conversion form. Returns: form_values (Dict[str, str | float] | None)"""
        self.form = st.form("conversion_form")
        with self.form:
            self.form_values["from_currency"] = st.selectbox("From Currency:", ['EUR'])
            self.form_values["to_currency"] = st.selectbox("To Currency:", CURRENCY_OPTIONS, index=CURRENCY_OPTIONS.index("USD"))
            self.form_values["amount"] = st.number_input("Enter the amount to convert")
            submit: bool = st.form_submit_button("Convert")
            
            if submit:
                if self.form_values["amount"] <= 0.00:
                    st.warning("Enter an amount higher than 0.00 and click [Convert]")
                    return
                self.annimation()
                return self.form_values

            st.info("Fill out the fields above and click [Convert]")
        return

    # Display the results of the conversion
    def display_result(self, from_currency: str, to_currency: str, amount: float, date: str, time: str,  result: float) -> None:
        """Displays the result of the currency conversion calculated from the api request"""
        # col1, col2 = st.columns(2,gap='small')
        # col1.write(f"As of {date_time}")
        # col2.write(f"{amount} {from_currency} = {result} {to_currency}")
        with self.form:
            st.success("Success!")
            st.subheader(f"{amount} {from_currency} = {result} {to_currency}", divider="green")
        st.text(f"""As of: {date} {time}""")