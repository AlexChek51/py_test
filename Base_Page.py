from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))
    
    def click_element(self, by, locator):
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()
        return element

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_current_url(self):
        return self.driver.current_url
    
    def switch_to_new_tab(self):
        original_window = self.driver.current_window_handle
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_window = [window for window in self.driver.window_handles if window != original_window][0]
        self.driver.switch_to.window(new_window)
