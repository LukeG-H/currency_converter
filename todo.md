# ToDo

### Form UI:

- [x] Implement form as a class
- [x] Collect / return form inputs as a Dict (form_values)
- [x] Add status elements to form on submit
- [x] Move if submit statement inside the form
- [x] Improve display_error method to handle warnings as well

### Exchange API:

- [x] Implement exchange api as a class
- [] Create an APIClient class to handle create_api_request & send_api_request (better encapsulation + avoid streamlit caching error with 'self')
- [] Create a test_api_response method for testing invalid responses
- [] Move create_api_request into exchange api class

### API Request Builder:

- [] Create HTTPRequestBuilder class
  - [] self.url: str = ""
  - [] self.method: string = "GET"
  - [] self.headers: Dict[str, str] = {}
  - [] self.body: Any = null
  - [] self.timeout: int = 5000
  - [] self.retries: int = 0
- [] Create Methods for constructing an API Request
  - [] set_url(self, url: str): self.url = url return self
  - [] set_method(self, method: str): self.method = method return self
  - [] add_header(self, key: str, value: str) self.headers[key] = value return self
  - [] set_body(self, body: Any) self.body = body return self
  - [] set_timeout(self, timeout: int) self.timeout = timeout return self
  - [] set_retries(self, retries: int) self.retries = retries return self
  - [] build(self):
    url = f" \
     {self.url}...
    self.method,
    self.headers,
    {}, # query params
    self.body,
    self.timeout,
    self.retries,
    True
