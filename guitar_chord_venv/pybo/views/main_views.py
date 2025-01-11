from flask import Blueprint
from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

bp = Blueprint('main', __name__, url_prefix='/')
#url_prefix='/' 대신 url_prefix='/main'이라고 입력했다면 hello_pybo 함수를 호출하는 URL은 localhost:5000/이 아니라 localhost:5000/main/이 된다.


@bp.route('/')
def index():
    
    return render_template('index.html')

@bp.route('/search',methods=['POST'])
def search():
    query= request.form['query']
    image_urls = crawl_images(query)
    
    print("good111")
    crawl_images2(query)
    return render_template('result.html',images = image_urls)

def crawl_images(query):
    url = f"https://www.google.com/search?hl=ko&tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all('img')
    image_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    print("checking!!!!!!",image_urls[0])
    return image_urls[:10]  # 상위 10개 이미지만 반환

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def crawl_images2(query):
    print('crawl2222222')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    url = f"https://www.google.com/search?hl=ko&tbm=isch&q={query}"
    
 
    driver.get(url)
    #WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'YQ4gaf')]/img")))
    
    img_elements = driver.find_elements(By.XPATH, "//img[contains(@class, 'YQ4gaf')]")[:5]
    
    print("good222")
    
    iurl=[]
    for img in img_elements:
        iurl = img.get_attribute('src')
    print(iurl)    
        
    driver.quit()
    return iurl

#셀레니움을 사용해서 값은 다 뽑히는데 문제는 1 번 크롤링은 사이트로 해서 이미지가 다 나오는데 
#2번셀레니뭄 크롤링은 값이 나오지 않는다.data:image/png;base64 이런 형태라서 추출이 안되는 것 이부분을 더 찾아보기 