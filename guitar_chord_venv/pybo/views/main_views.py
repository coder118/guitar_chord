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
    
    try:
        chords = [item.strip() for item in query.split(',')]
        print("chords",chords)
        image_urls=[]
        for c in chords:
            image_urls.append(crawl_images2("기타"+ c + "코드" ))
        #image_urls = crawl_images_for_chords(chords)
    except:# 쿼리문내부에 콤마로 문자열이 나뉘지 않은경우
        image_urls = crawl_images2("기타 "+ query + "코드")
    
    print("good111")
    #crawl_images2(query)
    #print("imageurl",image_urls)
    return render_template('result.html',images = image_urls, query=chords)

# from concurrent.futures import ThreadPoolExecutor

# def crawl_images_for_chords(chords):
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(crawl_images2, ["기타 " + chord + " 코드" for chord in chords]))
#     return results


def crawl_images(query):
    url = f"https://www.google.com/search?hl=ko&tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    #print('response',response)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print('soup',soup)
    img_tags = soup.find_all('img')
    image_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    #print("checking!!!!!!",image_urls)
    return image_urls[:10]  # 상위 10개 이미지만 반환

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def crawl_images2(query):
    print('crawl2222222')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    from urllib.parse import quote
    encoded_query = quote(query) #기타의 #같은 특수문자를 인식을 못해서 인코딩해줌
    url = f"https://www.google.com/search?hl=ko&tbm=isch&q={encoded_query}"
    
 
    driver.get(url)
    WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'YQ4gaf')]")))
    
    img_elements = driver.find_elements(By.XPATH, "//img[contains(@class, 'YQ4gaf')]")#[contains(@class, 'YQ4gaf')]
    
    print("good222")
    #print('img_elements',img_elements)
    iurl=[]
    i=0 #보니까 img_elements에서 이미지를 제한을 해버리면 그 페이지에 있는 이상한 이미지들도 전부다 가져와버린다. 그래서 i를 이용해 3장이상 추가되지 않게끔 바꿈/ 여기서 조정을 할 수 있는 기능을 넣어도 좋겟다.
    for img in img_elements:
        img_url = img.get_attribute('src')  # URL 추출
        
        alt_text = img.get_attribute('alt') #유튜브 섬네일이미지가 추출되는것을 방지하기 위함 alt요소에 항상 사이트의 출처가 적힌 특징이있었음
       
        natural_width = int(img.get_attribute('naturalWidth'))  # 'YQ4gaf' 이 클래스에 내가원하지 않는 이미지들이 존재해서 사이즈가 너무 작은 이미지들은 거르기 위해 사용
        natural_height = int(img.get_attribute('naturalHeight'))
        
        if img_url and not (natural_width < 100 and natural_height <100) and "YouTube" not in alt_text:  # 높이 넓이가 100픽셀 이하면 이미지 url에 추가하지 않는다. /유튜브 섬네일도 추가 안함
            iurl.append(img_url)  # 리스트에 추가
            i+=1
            if i==5:#5개의 이미지 추출
                break
    
    driver.quit()
    #print('iurl',iurl)
    return iurl

#셀레니움을 사용해서 값은 다 뽑히는데 문제는 1 번 크롤링은 사이트로 해서 이미지가 다 나오는데 
#2번셀레니뭄 크롤링은 값이 나오지 않는다.data:image/png;base64 이런 형태라서 추출이 안되는 것 이부분을 더 찾아보기 