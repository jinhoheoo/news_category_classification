#헤드라인 크롤링하려함.
#크롤링(스크라이핑)(데이터 긁어온다고 보면됨) 하는법
#뷰티풀숲이용해서 클래스를 가지고 타이틀을 가지고 온거임

from bs4 import BeautifulSoup  #크롤링 할 때 필요함.    #pip install bs4
import requests # 라이브러리를 현재의 파이썬 스크립트 또는 프로젝트에 가져옵니다. 이 라이브러리는 HTTP 요청을 보내고 받는 데 사용됩니다.
import re
import pandas as pd
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

#아래 코드는 어떻게하는지 보려고 실습한거임. ##이게 코드임
##url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
##resp = requests.get(url) #즉 클라이언트와 같음. 주소를 줘서 웹서버에 웹페이지를 요청함. 즉 주소 보내서 주소에 대한 HTML문서를 받아옴
#url: 요청을 보낼 대상 URL입니다.
#requests.get(): GET 메서드를 사용하여 웹 서버에 요청을 보내고, 서버로부터의 응답을 받아옵니다.
#이 응답은 보통 HTML 문서와 함께 웹 페이지의 내용을 포함하게 됩니다.
#서버는 이 요청에 대한 응답으로 여러 정보를 포함한 객체를 반환합니다. 이 객체는 resp 변수에 저장됩니다.
#resp.text를하면 저 url인 웹페이지의 HTML코드가 포함됨.

# 서버는 요청을 기다리는 애. 무언가의 요청을 기다리다 오면 거기에대한 응답을줌
# 클라이언트는 요청을 하는 애
#서버 (Server): 서버는 정보나 서비스를 제공하는 중앙 시스템. 서버만들때 주로 리눅스를 사용함.
#역할: 서비스를 제공하고, 클라이언트로부터 요청을 받아 처리하는 컴퓨터 또는 소프트웨어입니다.
#기능: 데이터, 파일, 웹페이지, 응용프로그램 등을 클라이언트에게 제공하거나, 클라이언트의 요청에 따라 특정 작업을 수행합니다.
#예시: 웹 서버는 웹페이지를 클라이언트 브라우저에게 제공하고, 파일 서버는 파일을 다운로드할 수 있게 해줍니다.

#클라이언트 (Client): 서버에서 제공되는 정보나 서비스를 이용하는 사용자나 소프트웨어입니다.
#역할: 서버에게 서비스나 데이터를 요청하고, 서버로부터 받은 데이터를 활용하는 컴퓨터 또는 소프트웨어입니다.
#기능: 사용자가 서버에서 제공하는 자원을 활용하거나, 서버에게 요청을 보내 데이터를 받아오는 등의 작업을 수행합니다.
#예시: 웹 브라우저는 웹 서버에게 웹페이지를 요청하고, 이를 표시하여 사용자에게 보여줍니다.
#이러한 서버-클라이언트 모델은 네트워크 상에서 다양한 종류의 데이터 및 서비스 교환을 가능케 하는 중요한 개념입니다.

##print(resp)
##print(type(resp))
##print(list(resp))

##soup = BeautifulSoup(resp.text, 'html.parser')
##print(soup)
##title_tags = soup.select('.sh_text_headline')#.sh 이렇게한 이유는 sh_text_headline 이라는클래스를 가진 에들을 select하려하고 함.
#저 클래스에들만 가져와서 리스트로 만든거임
##print(title_tags)
##print(len(title_tags))
##print(type(title_tags[0]))
##titles = []
##for title_tag in title_tags:
##    titles.append(re.compile('[^가-힣|a-z|A-Z]').sub('', title_tag.text))
    #re.compile('[^가-힣|a-z|A-Z]'): 정규 표현식 패턴을 정의합니다. 여기서 ^는 부정을 의미하고, 가-힣은 한글, a-z는 영문 소문자, A-Z는 영문 대문자를 나타냅니다.
    # 따라서 이 패턴은 한글과 영문 대소문자를 제외한 문자를 찾아냅니다. 즉 띄어쓰기 이런거 찾는거임.
    #.sub('', title_tag.text): 찾아낸 패턴을 빈 문자열로 대체합니다. 즉''이거니까 빈 문자열로 바꾼다는거임.
    # 이로써 해당 패턴에 매치되는 문자들이 모두 제거됩니다.
    #replace는 특정 문자를 찾아서 바꾸는거고 re는 특정문자를 찾는거고 거기에 sub를 붙여서 찾은거를 빼는거임.
##print(titles)

df_titles = pd.DataFrame()  #데이터프레임 형태 만들어서 타이틀이랑 카테고리 넣으려함.
re_title = re.compile('[^가-힣|a-z|A-Z]') #텍스트 가져올때 가져오려고하는부분만 가져올려고
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
#이렇게 headers 이런식으로 하면 웹브라우저에서 요청한줄알고 크롤링을 웹페이지에서 막지않음. 트래픽관리한다고 크롤링 막아놓는경우가 있어서 이렇게함.

for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i) #이렇게 url저장
    resp = requests.get(url, headers = headers)     #이렇게해서 url에 맞는 브라우저 가져오려고
    # 이 부분에서는 requests 라이브러리를 사용하여 위에서 생성한 URL에 HTTP GET 요청을 보냅니다. headers 매개변수를 사용하여 요청에 헤더 정보를 추가할 수 있습니다.
    # 이 경우, 브라우저처럼 보이도록 하는 헤더가 headers 변수에 저장되어 있을 것입니다.
    soup = BeautifulSoup(resp.text, 'html.parser')  #이걸로 브라우저 킴
    #라이브러리를 사용하여 HTML 문서를 파싱합니다. resp.text는 HTTP 응답에서 얻은 HTML 문서의 텍스트 내용을 나타냅니다.
    # 'html.parser'는 BeautifulSoup에서 사용할 파서의 종류를 지정합니다.
    title_tags = soup.select('.sh_text_headline')   #클래스 이용해서 원하는 텍스트 부분만 가져옴.
    titles = []
    for title_tag in title_tags:
        titles.append(re_title.sub(' ', title_tag.text))    #타이틀가져올때 필요없는부분없앰
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i] #카테고리 열을 추가해줌
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows',
                          ignore_index=True) #concat해서 타이틀열과 카테고리열을 합친 df_titles를 만들어줌
    #pd.concat(): pandas에서 제공하는 DataFrame을 합치는 함수입니다.
    #[df_titles, df_section_titles]: 합쳐질 DataFrame들을 리스트로 전달합니다. 여기서는 df_titles와 df_section_titles가 두 개의 DataFrame으로 전달되었습니다.
    #axis='rows': 합치는 방향을 지정합니다. 'rows'는 행 방향으로 합침을 의미합니다. 수평으로 합치려면 'columns'을 사용할 수 있습니다.
    #ignore_index=True: 인덱스를 무시하고 새롭게 인덱스를 부여합니다. 이 옵션을 사용하면 새롭게 합쳐진 DataFrame의 인덱스가 0부터 시작하게 됩니다.

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index= False)
#to_csv(): DataFrame을 CSV 파일로 저장하는 pandas의 메서드입니다.
#'./crawling_data/naver_headline_new_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')):
# 저장될 CSV 파일의 경로와 파일 이름을 지정합니다. 여기서 {}에는 현재 날짜를 넣기 위해 datetime.datetime.now().strftime('%Y%m%d')를 사용하고 있습니다.
# 예를 들어, 파일 이름이 "naver_headline_new_20220123.csv"와 같이 날짜가 포함됩니다.
#index=False: CSV 파일에 DataFrame의 인덱스를 저장하지 않도록 설정합니다. CSV 파일에 인덱스가 저장되면 파일을 다시 읽을 때 추가적인 열로 인식됩니다.
