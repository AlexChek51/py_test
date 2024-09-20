import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Page_Objects import MainPage
from Page_Objects import ContactsPage
from Page_Objects import TensorPage
from Page_Objects import DownloadPage
from time import sleep


@pytest.fixture
def driver():
    download_dir = os.path.join(os.getcwd(), 'downloads')

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    options = Options()
    options.add_argument("--start-maximized")
    prefs = {"download.default_directory": download_dir, "download.prompt_for_download": False}
    options.add_experimental_option("prefs", prefs)

    service = Service('E:/PythonProjects/test/chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://sbis.ru/")
    yield driver
    driver.quit()

def test_scenario_1(driver):
    main_page = MainPage(driver)
    contacts_page = ContactsPage(driver)
    tensor_page = TensorPage(driver)

    main_page.go_to_contacts()
    contacts_page.click_tensor_link()
    contacts_page.switch_to_new_tab()
    sleep(2)
    
    assert contacts_page.get_current_url() == "https://tensor.ru/", "Неверный URL"
    assert tensor_page.verify_block_text() == "Сила в людях", "Неверный текст"
    tensor_page.click_more_link()
    assert contacts_page.get_current_url() == "https://tensor.ru/about", "Неверный URL"
    
    # Проверка изображений в разделе "Работаем"
    tensor_page.verify_work_section_images()

    print("Все изображения имеют одинаковую ширину и высоту.")

def test_scenario_2(driver):
    main_page = MainPage(driver)
    contacts_page = ContactsPage(driver)

    main_page.go_to_contacts()
    assert contacts_page.get_current_region() == "Пермский край", "Неверный регион"
    contacts_page.change_region("41 Камчатский край")
    sleep(1)
    assert contacts_page.get_current_region() == "Камчатский край", "Неверный регион"

    # Проверка URL и title
    assert "41-kamchatskij-kraj" in contacts_page.get_current_url(), f"URL не содержит '41-kamchatskij-kraj': {contacts_page.get_current_url()}"
    assert "СБИС Контакты — Камчатский край" in driver.title, f"Title не содержит 'СБИС Контакты — Камчатский край': {driver.title}"

    print("Регион изменен на Камчатский край. Список партнеров обновлен. URL и title содержат информацию выбранного региона")

def test_scenario_3(driver):
    main_page = MainPage(driver)
    download_page = DownloadPage(driver)

    main_page.go_to_downloads()
    download_page.select_plugin_for_windows()
    download_page.click_download_button()
    sleep(60)  # Увеличим время ожидания для завершения загрузки
    
    download_dir = os.path.join(os.getcwd(), 'downloads')
    downloaded_files = os.listdir(download_dir)
    assert len(downloaded_files) > 0, "Файл не был загружен"

    # Проверка размера загруженного файла
    file_path = os.path.join(download_dir, downloaded_files[0])
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    expected_size_mb = 11.45
    assert abs(file_size_mb - expected_size_mb) < 0.1, f"Размер файла {file_size_mb:.2f} МБ отличается от ожидаемого {expected_size_mb} МБ"

    print("Файл успешно загружен и размер соответствует ожидаемому.")
