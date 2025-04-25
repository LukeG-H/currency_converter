import streamlit as st
import time
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from currencies import CURRENCY_OPTIONS
from typing import *


class FormUi:
    def __init__(self):
        self.form_values: Dict[str, str | float | None] = {
            "from_currency": None,
            "to_currency": None,
            "amount": None
            }
        self.title()

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

    def form_has_valid_input(self) -> bool:
        """
        Validates: form values are populated, amount is either an int or float, and amount is greater than 0.
        Returns: True | False
        """
        values = self.form_values
        if not values:
            return False
        if not isinstance(values.get("amount"), (int, float)):
            return False
        return values["amount"] > 0

    def annimation(self) -> None:
        """Annimation displayed on Submission of the form"""
        rain(
            emoji = "💱",
            font_size = 60,
            falling_speed = 4,
            animation_length = 1,
        )
    
    def conversion_form(self) ->  None:
        """Main currency conversion form. Updates form_values if input is valid"""
        self.form = st.form("conversion_form")
        with self.form:
            from_currency: str = st.selectbox("From Currency:", ['EUR'])
            to_currency: str = st.selectbox("To Currency:", CURRENCY_OPTIONS, index=CURRENCY_OPTIONS.index("USD"))
            amount: float = st.number_input("Enter the amount to convert")
            submit: bool = st.form_submit_button("Convert")
            
            if submit:
                self.form_values["from_currency"] = from_currency
                self.form_values["to_currency"] = to_currency
                self.form_values["amount"] = amount

                if not self.form_has_valid_input():
                    st.warning("Enter an amount higher than 0.00 and click [Convert]")
                    return
                return
            st.info("Fill out the fields above and click [Convert]")
        return

    def display_result(
        self, 
        from_currency: str, 
        to_currency: str, 
        amount: float, 
        date: str, 
        time: str, 
        result: float
    ) -> None:
        """Displays the result of the currency conversion calculated from the API request"""
        with self.form:
            st.success("Success!")
            self.annimation()
            
            st.subheader(
                f"*{amount:,.2f}* :blue[{from_currency}] = *{result:,.2f}* :blue[{to_currency}]", 
                divider="green"
            )
        st.caption(f"As of: {date} {time}")

    def display_error(self, message: str) -> None:
        """Displays an error message in the UI if something goes wrong"""
        st.error(message)