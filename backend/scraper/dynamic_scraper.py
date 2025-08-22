from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

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

        body_text = driver.find_element(By.TAG_NAME, "body").text

        driver.quit()
        return {"html": body_text}
    except Exception as e:
        return {"error": str(e)}
