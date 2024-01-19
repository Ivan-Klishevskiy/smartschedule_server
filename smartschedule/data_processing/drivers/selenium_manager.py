# from typing import Optional, List

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# from webdriver_manager.chrome import ChromeDriverManager

# class SeleniumManager:

#     def setup_driver() -> Optional[webdriver.Chrome]:
#         try:
#             options = Options()
#             options.add_argument('--headless')
#             options.add_argument("--lang=en")  # Set browser language to English
#             options.add_experimental_option("excludeSwitches", ["enable-logging"])
#             driver = webdriver.Chrome(options=options)
#             return driver
#         except Exception as e:
#             logging.error(f"Failed to setup WebDriver: {e}")
