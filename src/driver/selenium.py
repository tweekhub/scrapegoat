from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium import webdriver
from . import logger

from typing import Dict, List, Optional
import time
import os
import sys
import platform

class UIElement:
    def __init__(self, element_data: Dict[str, str]):
        self.element_type: str = element_data.get('element_type', '')
        self.selector_type: str = element_data.get('selector_type', '')
        self.selector_value: str = element_data.get('selector_value', '')
        self.action: str = element_data.get('action', '')
        self.post_action: str = element_data.get('post_action', '')

    def to_dict(self) -> Dict[str, str]:
        return {
            'element_type': self.element_type,
            'selector_type': self.selector_type,
            'selector_value': self.selector_value,
            'action': self.action,
            'post_action': self.post_action,
        }

class BrowserClient:
    def __init__(self, timeout_after: int = 15, max_retries: int = 5, browser_headless: bool = False, is_experimental: bool = False):
        self.driver: Optional[webdriver.Chrome] = None
        self.initial_window_handle: Optional[str] = None
        self.timeout_after = timeout_after
        self.max_retries = max_retries
        self.browser_headless = browser_headless
        self.is_experimental = is_experimental

    def initialize_driver(self):
        options = self._configure_chrome_options()
        service = self._get_chrome_service(options)
        
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.initial_window_handle = self.driver.current_window_handle
            logger.debug(f"Successfully Initialized Chrome Browser with Initial Window Handle: {self.initial_window_handle}")
        except WebDriverException as error:
            logger.error(f"Failed to initialize Chrome browser: {error}")
            logger.error("Ensure that the Chrome Portable and ChromeDriver binaries are correctly bundled.")

    def _configure_chrome_options(self) -> Options:
        options = Options()
        if self.browser_headless:
            options.add_argument("--headless")
            logger.debug("Headless mode enabled")

        default_arguments = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--window-size=1450,860",
            "--password-store=basic",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        ]
        
        for arg in default_arguments:
            options.add_argument(arg)

        if self.is_experimental:
            experimental_options = [
                ("excludeSwitches", ["enable-automation"]),
                ("useAutomationExtension", False),
                ("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
            ]
            for option, value in experimental_options:
                options.add_experimental_option(option, value)
            logger.debug("Experimental options added")

        logger.debug(f"Chrome configured with options: {options.arguments}")
        return options

    def _get_chrome_service(self, options: Options) -> Service:
        current_platform = platform.system().lower()
        is_bundled = getattr(sys, 'frozen', False)

        if is_bundled:
            chrome_path = os.path.join(sys._MEIPASS, 'chrome_portable')
            chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver')
        else:
            chrome_path = os.path.join(os.getcwd(), 'chrome', 'browser')
            chromedriver_path = os.path.join(os.getcwd(), 'chrome')

        if current_platform.startswith('win'):
            chrome_binary = 'chrome.exe'
            chromedriver_binary = 'chromedriver.exe'
        elif current_platform.startswith('linux') or current_platform.startswith('darwin'):
            chrome_binary = 'chrome'
            chromedriver_binary = 'chromedriver'

        chrome_binary_path = os.path.join(chrome_path, chrome_binary)
        chromedriver_binary_path = os.path.join(chromedriver_path, chromedriver_binary)

        service = Service(executable_path=chromedriver_binary_path)
        options.binary_location = chrome_binary_path

        return service

    def open_new_tab(self, url: str):
        if self.driver:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(url)
            logger.debug(f"Opening New Tab for URL: {url} Total Tabs: {len(self.driver.window_handles)}")

    def switch_to_tab(self, index: int):
        if self.driver:
            logger.debug(f"Switching to tab index: {index}")
            if index < len(self.driver.window_handles):
                self.driver.switch_to.window(self.driver.window_handles[index])
                logger.debug(f"Switched to tab with handle: {self.driver.current_window_handle}")
            else:
                logger.warning(f"Tab index {index} is out of range. Total tabs: {len(self.driver.window_handles)}")

    def open_page_in_same_tab(self, url: str):
        if self.driver:
            logger.debug(f"Navigating to {url}")
            try:
                self.driver.get(url)
                logger.debug(f"Successfully Navigated to {url}")
            except Exception as e:
                logger.error(f"Failed to Navigate to {url}: {e}")

    def located_element(self, selector_value: str, selector_type: str):
        locator = (self._get_by_selector(selector_type), selector_value)
        return CachedWebElement(locator)

    def process_elements_chain(self, elements: List[UIElement]):
        logger.debug(f"Processing {len(elements)} Elements Chain")
        for element in elements:
            self.process_element(element, self.max_retries)

    def process_element(self, element: UIElement, retries: int):
        logger.debug(f"Processing element: {element.to_dict()}")
        try:
            found_element = self.wait_and_find_element(element.selector_value, element.selector_type)
            found_element = self.scroll_to_element(found_element)
            found_element = self._perform_action(element, found_element)
            if element.post_action:
                found_element = self._perform_post_action(element, found_element)
            time.sleep(1)
            logger.debug(f"Successfully Processed UIElement {element.element_type}")
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            if retries > 0:
                logger.warning(f"Error interacting with UIElement '{element.element_type}': {str(e)}. Retrying {retries} more times.")
                self.process_element(element, retries - 1)
            else:
                logger.error(f"Failed to process UIElement with selector '{element.element_type}' after multiple retries: {e}")
        except Exception as e:
            logger.error(f"Failed to process UIElement with selector '{element.element_type}': {e}")

    def wait_and_find_element(self, selector_value: str, selector_type: str) -> WebElement:
        if self.driver:
            logger.debug(f"Waiting {self.timeout_after} seconds to find WebElement using UIElement: {selector_value}")
            WebDriverWait(self.driver, self.timeout_after).until(
                EC.presence_of_element_located((self._get_by_selector(selector_type), selector_value))
            )
            element = self.driver.find_element(self._get_by_selector(selector_type), selector_value)
            logger.debug(f"Found WebElement! name={element.accessible_name}, tag={element.tag_name}")
            return element
        else:
            raise WebDriverException("Driver is not initialized")

    def scroll_to_element(self, element: WebElement) -> WebElement:
        if self.driver:
            logger.debug(f"Scrolling to name={element.accessible_name}, tag={element.tag_name}")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.debug("Scrolled Successfully!")
            return element
        else:
            raise WebDriverException("Driver is not initialized")

    @staticmethod
    def _get_by_selector(selector: str):
        selector_map = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "link": By.LINK_TEXT,
            "partial": By.PARTIAL_LINK_TEXT
        }
        selector_type = selector.lower().split(':')[0]
        return selector_map.get(selector_type, By.NAME)

    def _perform_action(self, element: UIElement, found_element: WebElement) -> WebElement:
        logger.debug(f"Performing action={element.action} on UIElement={element.selector_value}")
        if element.action == 'click':
            found_element.click()
        elif element.action == 'USE_SCRIPT':
            self.driver.execute_script("arguments[0].click();", found_element)
        logger.debug(f"Action {element.action} performed successfully")
        return found_element

    def _perform_post_action(self, element: UIElement, found_element: WebElement) -> WebElement:
        logger.debug(f"Performing post-action={element.post_action} on UIElement={element.selector_value}")
        if element.post_action == 'submit':
            found_element.submit()
        logger.debug(f"Post-action {element.post_action} performed successfully")
        return found_element

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.initial_window_handle = None
            logger.info("Chrome Browser closed successfully!")
        else:
            logger.warning("Driver is not initialized!")