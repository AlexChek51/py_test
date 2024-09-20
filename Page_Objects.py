from selenium.webdriver.common.by import By
from Base_Page import BasePage

class MainPage(BasePage):
    CONTACTS_LINK = (By.LINK_TEXT, "Контакты")
    DOWNLOAD_LINK = (By.LINK_TEXT, "Скачать локальные версии")
    
    def go_to_contacts(self):
        self.click_element(*self.CONTACTS_LINK)

    def go_to_downloads(self):
        self.click_element(*self.DOWNLOAD_LINK)

class ContactsPage(BasePage):
    TENSOR_LINK = (By.CSS_SELECTOR, 'a.sbisru-Contacts__logo-tensor')
    REGION_SELECTOR = (By.CSS_SELECTOR, "span.sbis_ru-Region-Chooser__text")
    
    def click_tensor_link(self):
        self.click_element(*self.TENSOR_LINK)
    
    def change_region(self, region_name):
        self.click_element(*self.REGION_SELECTOR)
        region_option = self.find_element(By.XPATH, f"//span[text()='{region_name}']")
        self.driver.execute_script("arguments[0].click();", region_option)

    def get_current_region(self):
        return self.find_element(*self.REGION_SELECTOR).text

    def get_current_url(self):
        return self.driver.current_url

class TensorPage(BasePage):
    BLOCK_TEXT = (By.CSS_SELECTOR, "div.tensor_ru-Index__block4-content.tensor_ru-Index__card")
    MORE_LINK = (By.CSS_SELECTOR, "a.tensor_ru-link.tensor_ru-Index__link")
    WORK_SECTION = (By.CSS_SELECTOR, "div.tensor_ru-About__block3")

    def verify_block_text(self):
        block = self.find_element(*self.BLOCK_TEXT)
        self.scroll_to_element(block)
        paragraph = block.find_element(By.CSS_SELECTOR, "p.tensor_ru-Index__card-title.tensor_ru-pb-16")
        return paragraph.text
    
    def click_more_link(self):
        block = self.find_element(*self.BLOCK_TEXT)
        more_link = block.find_element(*self.MORE_LINK)
        more_link.click()

    def verify_work_section_images(self):
        work_section = self.find_element(*self.WORK_SECTION)
        images = work_section.find_elements(By.TAG_NAME, 'img')

        if not images:
            raise AssertionError("Изображения не найдены в разделе 'Работаем'")

        first_image_width = images[0].size['width']
        first_image_height = images[0].size['height']

        for image in images:
            assert image.size['width'] == first_image_width, "Разная ширина у изображений!"
            assert image.size['height'] == first_image_height, "Разная высота у изображений!"

class DownloadPage(BasePage):
    PLUGIN_LINK = (By.CSS_SELECTOR, "div.controls-TabButton__caption")
    DOWNLOAD_BUTTON = (By.CSS_SELECTOR, "a.sbis_ru-DownloadNew-loadLink__link.js-link")

    def select_plugin_for_windows(self):
        self.click_element(*self.PLUGIN_LINK)
    
    def click_download_button(self):
        self.click_element(*self.DOWNLOAD_BUTTON)
