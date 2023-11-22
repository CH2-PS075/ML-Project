from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time
import os

def find_data_bing(text, count, main_path, clas):

    path = os.getcwd()
    try:
        os.mkdir(os.path.join(path, main_path))
    except:
        pass

    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.bing.com/images/feed?form=Z9LH")
    text = text
    driver.find_element(By.CLASS_NAME, 'b_searchbox').clear()
    driver.find_element(By.CLASS_NAME, 'b_searchbox').send_keys(text)
    driver.find_element(By.CLASS_NAME, 'b_searchbox').submit()

    driver.find_element(By.ID, 'fltIdtLnk').click()
    i = driver.find_element(By.XPATH, '//span[@title="Image size filter"]')

    time.sleep(5)
    i.click()
    driver.find_element(By.XPATH, '//a[@title="Extra large"]').click()

    imgs = driver.find_elements(By.XPATH, '//div/a/div/img')
    counts = count
    while len(imgs) < counts+1:
        imgs = driver.find_elements(By.XPATH, '//div/a/div/img')
        try:
            driver.find_element(By.XPATH, '//div/a[@class="btn_seemore cbtn mBtn"]').click()
        except:
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")

    imgs = [i.get_attribute('src') for i in imgs]

    try:
        os.mkdir(os.path.join(path, main_path, clas))
    except:
        pass  

    cnt = 1
    for i in imgs:
        try:
            response = requests.get(i)
            with open(f"{main_path}/{clas}/{text}_{cnt}.jpg","wb") as file:
                file.write(response.content)
            time.sleep(0.5)
            cnt += 1
        except:
            pass
        if cnt == count:
            break

if __name__ == "__main__":

    print("type classification:")
    clas = str(input())
    print("type the browser keywords:")
    text = str(input())
    print("how many data do you want to download ?")
    counts = int(input())
    print("type main path")
    main_path = str(input())
    find_data_bing(text, counts, main_path, clas)