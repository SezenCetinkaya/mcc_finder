from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

def get_dynamic_content(url):
    try:
        options = Options()
        options.headless = True
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        # ChromeDriver path
        driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(3)  # wait for the page to load

        html_content = driver.page_source

        driver.quit()
        return {"html": html_content}

    except Exception as e:
        return {"error": str(e)}
