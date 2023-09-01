from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from datetime import datetime, timedelta


class TestFlightBooking(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://www.mytrip.com/rf/start")

    def tearDown(self):
        self.driver.quit()

    def test_page_load_successful(self):
    # Arrange: setUp

    # Act: Check for the precence of <h1 data-testid="page-not-found-title">  which indicates the page wasn't found,
    # despite receiving 200 status code
        try:
            h1_attribute = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='page-not-found-title']")))
        except (NoSuchElementException, TimeoutException):
            h1_attribute = None

    # Assert: Check if the element is abscent (indicating successful page load)
        self.assertIsNone(h1_attribute)


    def test_departure_selection(self):
    # Arrange
        departure_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                ((By.ID, "searchForm-singleBound-origin-input"))))

    # Act
        departure_input.send_keys("ea")
        departure_input.click()
        departure_input.send_keys(Keys.ENTER)

        try:
            departure = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@data-testid='searchForm-singleBound-origin-input']//div[@class=' css-sdspv8-singleValue']"))).text
        except TimeoutException:
            departure = None

    # Assert
        self.assertIsNotNone(departure)   # indicating sucessful selection


    def test_arrival_selection(self):
    # Arrange
        arrival_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                ((By.ID, "searchForm-singleBound-destination-input"))))

    # Act
        arrival_input.send_keys("ge")
        arrival_input.click()
        arrival_input.send_keys(Keys.ENTER)

        try:
            departure = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@data-testid='searchForm-singleBound-destination-input']//div[@class=' css-sdspv8-singleValue']"))).text
        except TimeoutException:
            departure = None

    # Assert
        self.assertIsNotNone(departure)    # indicating successful selection


    def test_submit_form(self):
    # Arrange
        departure_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                ((By.ID, "searchForm-singleBound-origin-input"))))
        departure_input.send_keys("Eagle")
        departure_input.click()
        departure_input.send_keys(Keys.ENTER)

        arrival_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            ((By.ID, "searchForm-singleBound-destination-input"))))

        arrival_input.send_keys("Gebe")

        arrival_dropdown = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='etiDropdownOption']")))
        arrival_input.click()
        arrival_input.send_keys(Keys.ENTER)

        return_date_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.ID, "singleBound.returnDate")))

        test_date = datetime.now() + timedelta(days=3)
        test_date_str = test_date.strftime("%Y-%m-%d")
        self.driver.execute_script(f"arguments[0].value = '{test_date_str}'", return_date_input)
        print(test_date_str)

    # Act
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='searchForm-searchFlights-button']")
        submit_button.click()

    # Assert
        current_page = self.driver.current_url
        expected_page = "https://www.mytrip.com/rf/result"
        self.assertEqual(current_page, expected_page)


if __name__ == "__main__":
    unittest.main()

