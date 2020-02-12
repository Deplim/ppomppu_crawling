import requests
from bs4 import BeautifulSoup

#https://www.fun-coding.org/crawl_basic2.html

lv1_url = 'https://news.v.daum.net/v/20170615203441266'
html = requests.get(lv1_url).text
#print(html)
soup = BeautifulSoup(html, 'html.parser')

for a_tag in soup.select('.txt_info'):
    print(type(a_tag))
    print(a_tag.text)


# 1) reqeusts 라이브러리를 활용한 HTML 페이지 요청
# 1-1) res 객체에 HTML 데이터가 저장되고, res.content로 데이터를 추출할 수 있음
res = requests.get('http://v.media.daum.net/v/20170615203441266')

# print(res.content)
# 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
# 2-1) BeautifulSoup 파싱방법
soup = BeautifulSoup(res.content, 'html.parser')

# 3) 필요한 데이터 검색
title = soup.find('title')

# 4) 필요한 데이터 추출
print(type(title))
print(title.get_text())
