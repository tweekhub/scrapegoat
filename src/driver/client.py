import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumClient:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def close(self):
        """Close the browser and clean up."""
        self.driver.quit()



# Example usage
# if __name__ == '__main__':
#     client = SeleniumClient(headless=False)
#     client.visit('https://example.com')

#     # Example: Interact with an element
#     client.click_element(By.ID, 'example-button')

#     # Example: Handle CAPTCHA if present
#     client.handle_captcha()

#     # Example: Handle an alert if present
#     client.handle_alert()

#     # Example: Access shadow DOM elements
#     shadow_element = client.handle_shadow_dom('#shadow-host', 'button#shadow-button')
#     if shadow_element:
#         shadow_element.click()

#     client.close()
