from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time
import os

URL = "https://www.bing.com/images/feed?form=Z9LH"

def make_dir(clas, main_path):

    path = os.getcwd()
    try:
        os.mkdir(os.path.join(path, main_path))
    except:
        pass
    try:
        os.mkdir(os.path.join(path, main_path, clas))
    except:
        pass

    print(f"sucessfuly create folder {main_path} with\
          \ncategory folder {clas}")
    
def check_img_url(imgs, count):

    imgs_able = []
    cnt = 0
    for i in imgs:
        try:
            i = i.get_attribute('src')
            requests.get(i)
            imgs_able.append(i)
            cnt += 1
        except:
            pass
        if cnt == count:
            break
    
    print(f"{len(imgs_able)} of {len(imgs)} urls are able to be converted as .jpg\
          \nif {len(imgs_able)} < {count}, find more image urls with different keyword text...")
    return imgs_able

def make_img_file(imgs, main_path, clas, text, count):

    cnt = 0
    for i in imgs:
        response = requests.get(i)
        with open(f"{main_path}/{clas}/{text}_{cnt+1}.jpg","wb") as file:
            file.write(response.content)
        cnt += 1
        if cnt == count:
            break
            
        print(f"{cnt} of {len(imgs)} .jpg files have been made, if {cnt} < {count}\
              \nfind more images with different keyword text...")

def find_data_bing(text, count, clas, train_path, test_path, train_size=0.75):

    make_dir(clas, train_path)
    make_dir(clas, test_path)

    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
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
    while len(imgs) < count+1:
        imgs = driver.find_elements(By.XPATH, '//div/a/div/img')
        try:
            driver.find_element(By.XPATH, '//div/a[@class="btn_seemore cbtn mBtn"]').click()
        except:
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    print(f"found {len(imgs)} of elements")

    imgs = check_img_url(imgs, count)
    driver.close()
    
    if len(imgs) > count:
        imgs = imgs[:count]

    train_portion = int(count * train_size)
    train_imgs = imgs[:train_portion]
    test_imgs = imgs[train_portion:]

    make_img_file(train_imgs, train_path, clas, text, len(train_imgs))
    make_img_file(test_imgs, test_path, clas, text, len(test_imgs))