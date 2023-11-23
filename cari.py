from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
import os

def play(clas, text, counts, main_path):

    count = 1

    path = os.getcwd()
    try:
        os.mkdir(os.path.join(path, main_path))
    except:
        pass

    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://images.google.com/")
    text = text
    driver.find_element(By.ID, 'APjFqb').clear()
    driver.find_element(By.ID, 'APjFqb').send_keys(text)
    driver.find_element(By.ID, 'APjFqb').submit()

    try:
        os.mkdir(os.path.join(path, main_path, clas))
    except:
        pass

    img = driver.find_elements(By.XPATH, '//div[@jsname="DeysSe"]/img')
    img = [i.get_attribute('src') for i in img]
    while count < counts+1:
        img = driver.find_elements(By.XPATH, '//div[@jsname="DeysSe"]/img')
        img = [i.get_attribute('src') for i in img]
        for i in range(len(img)):
            try:
                response = requests.get(img[i])
                with open(f"{main_path}/{clas}/{text}_{count}.jpg","wb") as file:
                    file.write(response.content)
                time.sleep(0.5)
                count += 1
            except:
                pass
            if count == counts+1:
                break
        try:
            driver.find_element(By.XPATH, '//input[@value="Show more results"]').click()
        except:
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")

if __name__ == "__main__":

    print("type classification:")
    clas = str(input())
    print("type the browser keywords:")
    text = str(input())
    print("how many data do you want to download ?")
    counts = int(input())
    print("type main path")
    main_path = str(input())
    play(clas, text, counts, main_path)