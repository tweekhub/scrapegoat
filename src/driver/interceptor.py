from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class SeleniumClientWithInterception:
    def __init__(self, headless=False):
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.request_interceptor = self._intercept_request
        self.last_request = None

    def close(self):
        """Close the browser and clean up."""
        self.driver.quit()

    def visit(self, url):
        """Visit the target URL."""
        self.driver.get(url)

    def click_element(self, by, value):
        """Click an element."""
        element = self.driver.find_element(by, value)
        element.click()

    def _intercept_request(self, request):
        """Intercept the HTTP request and store it."""
        self.last_request = request
        print(f"Intercepted request: {request.method} {request.url}")

    def get_last_request(self):
        """Return the last intercepted request."""
        return self.last_request

    def perform_action_and_intercept(self, by, value):
        """Perform an action and intercept the next HTTP request."""
        self.last_request = None  # Reset the last request
        self.click_element(by, value)

        # Wait for the request to be intercepted
        timeout = 10  # seconds
        while self.last_request is None and timeout > 0:
            timeout -= 1
            time.sleep(1)

        if self.last_request:
            print(f"Next request after action: {self.last_request.method} {self.last_request.url}")
        else:
            print("No request intercepted after the action.")

# Example usage
# if __name__ == '__main__':
#     client = SeleniumClientWithInterception(headless=False)
#     client.visit('https://example.com')

#     # Perform an action that triggers a request
#     client.perform_action_and_intercept(By.ID, 'example-button')

#     # Close the browser
#     client.close()
