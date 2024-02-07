#네이버의 경우 job01처럼 request로 크롤링하면 되지만 대부분의 다른페이지들의 경우 주소체계가 뒤죽박죽인 경우가 많아 for을 돌리는게 힘듬
#이번에는 브라우저로 접근해서 하나하나 클릭해서 현재보이는 페이지에서 긁어오려함.
# 셀레니움을 이용해서 xpath를 통해 타이틀을 읽어옴
#여기꺼 이해안되면 movie버전도 셀레니움으로 자세하게 했으니 그거 보면됨.

from selenium import webdriver  #pip install selenium
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager  #pip install webdriver_manager
from selenium.common.exceptions import NoSuchElementException   #페이지 잘 안켜지면 오류로 취급할 수 있음
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument('user_agent='+ user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
##pages = [164, 352, 556, 81, 107, 81] #각 페이지 900을 줘서 마지막 페이지를 찾는거임 페이지 칸애 900페이지까지 없으니 마지막 페이지로 이동함.
#페이지 전부다 가져올꺼면 이런식으로 하면되고 페이지수 +1하는 이유는 range해서 이용하려함
#근데 이렇게 학습하려는 데이터의 불균형이 있으면 작은걸 늘리던가 큰걸 줄이던가 이렇게해서 데이터 개수를 맞춰줘야함.
#여기서는 충분히 많으니 작은거에 맞추자 여기선 105개로 맞추자.
pages = [105, 105, 105, 81, 105, 81]

df_titles = pd.DataFrame()
for l in range(6):
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)

    titles = []
    for k in range(1,pages[l]): #즉 1페이지 다음 2페이지 다음 3페이지 이런식으로 접근하는거임.

        url = section_url + '#&date=%2000:00:00&page={}'.format(k)
        #https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=1 이거 의미함
        try:        #주소가 없다든가 할때 오류생길수있으니 그거 방지하려고
            driver.get(url)     #이걸로 브라우저 킴
            time.sleep(0.5)     #브라우저 로드되기를 0.5초간 기다림
        except:
            print('driver.get', l, k)   #driver.get에서 오류발생했고 어느 카테고리의 어느 페이지에서 문제 발생했는지를 표현한거임.



        for i in range(1,5):
            for j in range(1,6):
                try:
                    title = driver.find_element('xpath','//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i,j)).text
                    # //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a		/이거는 파일시스템에서 /이거임 /진행될수록 내부로 들어감
                    # 이거 어디서 복사하냐면 정치의 페이지에서 검사로 기사제목 클릭한후 그걸 copy XPATH로 복사해오면됨
                    # 페이지안에서 기사에제목에 접근하는 방법이 여러가지임 1번에서는 클래스로 접근했고 여기서는 XPATH로 접근함.
                    # //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a
                    # //*[@id="section_body"]/ul[1]/li[3]/dl/dt[2]/a
                    # //*[@id="section_body"]/ul[1]/li[5]/dl/dt[2]/a
                    # //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a		이런식이니 이중포문하면되겠다.
                    title = re.compile('[^가-힣]').sub('', title)
                    titles.append(title)
                except:
                    print('find element', l, k , i, j)  # 어떤 뉴스기사에서 문제생겼는지 표현해줌
        if k % 5 ==0: #5페이지 마다 저장하려고
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[l]
            df_section_title.to_csv('./crawling_data/data_{}_{}.csv'.format(l, k))
            titles=[]
driver.close()


#df_titles = pd.concat([df_titles, df_section_title],axis='rows',ignore_index=True)