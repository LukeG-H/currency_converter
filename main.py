from exchange_api import ExchangeAPI
from form_ui import FormUi
from typing import *


def main() -> None:
    ui: FormUi = FormUi()
    session: ExchangeAPI = ExchangeAPI(ui)
    session.run()


if __name__ == "__main__":
    main()