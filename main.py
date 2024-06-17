from audiototext import convert
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import requests

def saveFile(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)

def bypasser():
    options = Options()
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    
    try:
        driver.get("https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php")
        time.sleep(5)
        
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
        
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[contains(@title, "challenge expires in two minutes")]')))
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[2]'))).click()
        
        href = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rc-audio"]/div[7]/a'))).get_attribute('href')
        response = requests.get(href, stream=True)
        saveFile(response, "audio.wav")
        
        audio_response = convert()
        
        audio_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="audio-response"]')))
        audio_box.send_keys(audio_response)
        
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-verify-button"]'))).click()
        
        os.remove('audio.wav')
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

bypasser()