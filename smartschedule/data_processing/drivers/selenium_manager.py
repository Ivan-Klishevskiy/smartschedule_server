import logging
import time
from typing import Optional, List


from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import os

logger = logging.getLogger('func_log')


class SeleniumManager:
    """
        The SeleniumManager class provides a set of static methods to interact with web pages using Selenium WebDriver.

        This class encapsulates the common operations performed with Selenium, such as setting up the driver,
        opening URLs, finding elements, waiting for elements, and interacting with elements (clicking, sending keys, etc.).

        It also handles exceptions that may occur during these operations, logging them for debugging purposes.
    """

    @staticmethod
    def setup_driver() -> Optional[webdriver.Firefox]:
        try:
            os.environ['WDM_LOG_LEVEL'] = '0'
            LOGGER.setLevel(logging.WARNING)
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')  # Uncomment if you want a headless browser
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            return driver
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")

    @staticmethod
    def close(driver: webdriver.Chrome) -> None:
        try:
            driver.close()
        except Exception as e:
            logger.error(f"Failed to close WebDriver: {e}")

    @staticmethod
    def open_url(driver: webdriver.Chrome, url: str):
        try:
            driver.get(url)
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")

    @staticmethod
    def _wait_for_element(element, locator, timeout=10):
        try:
            return WebDriverWait(element, timeout).until(EC.presence_of_element_located(locator))
        except (NoSuchElementException, TimeoutException, Exception) as e:
            logger.error(f"Failed to wait for element: {e}")
        return None

    @staticmethod
    def wait_element_by_class_name(element, class_name: str, timeout=10):
        locator = (By.CLASS_NAME, class_name)
        return SeleniumManager._wait_for_element(element, locator, timeout)

    @staticmethod
    def wait_element_by_name(element, name: str, timeout: int = 10):
        locator = (By.NAME, name)
        return SeleniumManager._wait_for_element(element, locator, timeout)

    @staticmethod
    def wait_element_by_id(element, name: str, timeout: int = 10):
        locator = (By.ID, name)
        return SeleniumManager._wait_for_element(element, locator, timeout)

    @staticmethod
    def wait_element_by_css_selector(element, css_selector: str, timeout: int = 10):
        locator = (By.CSS_SELECTOR, css_selector)
        return SeleniumManager._wait_for_element(element, locator, timeout)

    @staticmethod
    def find_element(element, by: str, value: str):
        try:
            if element:
                return element.find_element(by, value)
        except Exception as e:
            logger.error(f"Failed to find element: {e}")
        return None

    @staticmethod
    def find_element_by_class_name(element, class_name: str):
        return SeleniumManager.find_element(element, By.CLASS_NAME, class_name)

    @staticmethod
    def find_element_by_name(element, name: str):
        return SeleniumManager.find_element(element, By.NAME, name)

    @staticmethod
    def find_element_by_css_selector(element, css_selector: str):
        return SeleniumManager.find_element(element, By.CSS_SELECTOR, css_selector)

    @staticmethod
    def find_element_by_tag_name(element, tag_name: str):
        return SeleniumManager.find_element(element, By.TAG_NAME, tag_name)

    @staticmethod
    def find_element_by_id(element, element_id: str):
        return SeleniumManager.find_element(element, By.ID, element_id)

    @staticmethod
    def find_element_by_xpath(element, xpath: str):
        return SeleniumManager.find_element(element, By.XPATH, xpath)

    @staticmethod
    def find_elements(element, by: str, value: str):
        try:
            if element:
                return element.find_elements(by, value)
        except Exception as e:
            logger.error(f"Failed to find elements: {e}")
        return None

    @staticmethod
    def find_elements_by_css_selector(element, css_selector: str):
        return SeleniumManager.find_elements(element, By.CSS_SELECTOR, css_selector)

    @staticmethod
    def find_elements_by_tag_name(element, tag_name: str):
        return SeleniumManager.find_elements(element, By.TAG_NAME, tag_name)

    @staticmethod
    def find_elements_by_id(element, element_id: str):
        return SeleniumManager.find_elements(element, By.ID, element_id)

    @staticmethod
    def find_elements_by_xpath(element, xpath: str):
        return SeleniumManager.find_elements(element, By.XPATH, xpath)

    @staticmethod
    def find_elements_by_name(element, name: str):
        return SeleniumManager.find_elements(element, By.NAME, name)

    @staticmethod
    def find_elements_by_class_name(element, name: str):
        return SeleniumManager.find_elements(element, By.CLASS_NAME, name)
    
    @staticmethod
    def get_attribute(element, attribute: str):
        if element:
            return element.get_attribute(name=attribute)
        return None

    @staticmethod
    def get_attributes(elements: List[WebElement], attribute: str):
        href_attributes = []
        if elements is not None:
            print(f"Number of elements: {len(elements)}")
            for element in elements:
                try:
                    href = element.get_attribute(attribute)
                    if href:
                        href_attributes.append(href)
                except Exception as ex:
                    logger.error(f"Failed to get href attribute: {ex}")
        return href_attributes

    @staticmethod
    def send_keys(element, value: str):
        try:
            element.send_keys(value)
        except Exception as e:
            logger.error(f"Failed to send keys to element: {e}")

    @staticmethod
    def execute_script(driver, script: str):
        try:
            driver.execute_script(script)
        except Exception as e:
            logger.error(f"Failed to execute script: {e}")

    @staticmethod
    def click_element(element):
        try:
            element.click()
        except Exception as e:
            logger.error(f"Failed to click: {e}")

    @staticmethod
    def clear_element(element):
        try:
            element.clear()
        except Exception as e:
            logger.error(f"Failed to clear: {e}")

    @staticmethod
    def wait_element_nonzero_size_by_id(driver, element_id: str, timeout: int = 10):
        try:
            locator = (By.ID, element_id)
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator))

            def nonzero_size(driver):
                size = driver.find_element(*locator).size
                return size['width'] > 0 and size['height'] > 0

            WebDriverWait(driver, timeout).until(nonzero_size)

            return element
        except TimeoutException:
            logger.error(
                f"Element with ID '{element_id}' did not have nonzero size within the specified timeout.")
        except Exception as e:
            logger.error(
                f"Failed to wait for element with ID '{element_id}': {e}")

        return None

    @staticmethod
    def wait_element_by_tag_name(element, tag_name: str, timeout: int = 10):
        locator = (By.TAG_NAME, tag_name)
        return SeleniumManager._wait_for_element(element, locator, timeout)

    @staticmethod
    def _wait_for_elements(element, locator, timeout=10):
        try:
            return WebDriverWait(element, timeout).until(EC.presence_of_all_elements_located(locator))
        except (NoSuchElementException, TimeoutException) as e:
            logger.exception(e)
        except Exception as e:
            logger.error(f"Failed to wait for elements: {e}")
        return None

    @staticmethod
    def wait_elements_by_class_name(element, class_name: str, timeout=10):
        locator = (By.CLASS_NAME, class_name)
        return SeleniumManager._wait_for_elements(element, locator, timeout)

    @staticmethod
    def wait_elements_by_tag_name(element, tag_name: str, timeout=10):
        locator = (By.TAG_NAME, tag_name)
        return SeleniumManager._wait_for_elements(element, locator, timeout)
    
    @staticmethod
    def scroll_page(Driver, CountScroll):
        scroll_pause_time = 2

        for _ in range(CountScroll):
            SeleniumManager.execute_script(Driver, "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
