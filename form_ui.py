import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from currencies import CURRENCY_OPTIONS, CURRENCY_OPTIONS_WITH_PLACEHOLDER, EUR_WITH_PLACEHOLDER
from typing import *
from dataclasses import dataclass

@dataclass
class FormValues:
    from_currency: str | None = None
    to_currency: str | None = None
    amount: float | None = None


class FormUi:
    def __init__(self):
        self.form_values = FormValues()
        self.title()

    def title(self) -> None:
        """Sets the page title (header)"""
        self.title = colored_header(
            label="Currency Converter",
            description="*Currency data updated hourly*",
            color_name="violet-70",
        )

    def annimation(self) -> None:
        """Annimation displayed on Submission of the form"""
        rain(
            emoji = "💱",
            font_size = 60,
            falling_speed = 6,
            animation_length = 1,
        )
    
    def conversion_form(self) ->  None:
        """Main currency conversion form. Updates form_values if input is valid"""
        self.form = st.form("conversion_form")
        with self.form:
            from_currency: str = st.selectbox("From Currency:", EUR_WITH_PLACEHOLDER, index=0)
            to_currency: str = st.selectbox("To Currency:", CURRENCY_OPTIONS_WITH_PLACEHOLDER, index=0)
            amount: float = st.number_input("Enter the amount to convert")
            submit: bool = st.form_submit_button("Convert")
            
            if submit:
                self.form_values.from_currency = from_currency
                self.form_values.to_currency = to_currency
                self.form_values.amount = amount

                if not self.form_has_valid_input():
                    self.display_error("warning", self.reject_reason)
                    return
                return
            st.info("Fill out the fields above and click [Convert]")

    def form_has_valid_input(self) -> bool:
        """
        Validates: form values are populated, amount is either an int or float, and amount is greater than 0.
        Returns: True | False
        """
        values = self.form_values
    
        if not values:
            self.reject_reason = "Values are missing"
            return False
        
        if values.from_currency not in CURRENCY_OPTIONS or values.to_currency not in CURRENCY_OPTIONS:
            self.reject_reason = "Invalid Currency - Please choose a currency from the list"
            return False
        
        if not values.amount > 0:
            self.reject_reason = "Invalid Amount - Please enter an amount greater than 0.00 and click [Convert]"
            return False
        
        return True

    def display_error(self, flag: str, message: str) -> None:
        """Displays an error message, or warning in the UI if something goes wrong. flag = ('error' | 'warning')"""
        match flag:
            case "warning":
                st.warning(message)
            case "error":
                st.error(message)

    def display_result(self, date: str, time: str, result: float) -> None:
        """Displays the result of the currency conversion calculated from the API request"""
        with self.form:
            st.success("Success!")
            self.annimation()
            
            amount = self.form_values.amount
            from_currency = self.form_values.from_currency
            to_currency = self.form_values.to_currency

            st.subheader(
                f"*{amount:,.2f}* :blue[{from_currency}] = *{result:,.2f}* :blue[{to_currency}]", 
                divider="green"
            )
        st.caption(f"As of: {date} {time}")