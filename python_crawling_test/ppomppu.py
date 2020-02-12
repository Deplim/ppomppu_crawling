import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

def isHangul(text):
    encText = text
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
    return hanCount > 0

def check_latest_update():
    url = 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu4&page_num=20&category=&search_type=sub_memo&keyword=%C4%B7%C7%CE'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    latest_update = soup.find("tr", {"class": "list1"}).find("nobr", {"class": "eng list_vspace"}).get_text()
    latest_update = latest_update.replace("/", "-")
    current_day = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)

    if (":" in latest_update):
        latest_update = current_day + " " + latest_update

    print("*** latest_update: " + latest_update + " ***");
    
    return latest_update

def check_crawling_target(a_tag, latest_update):
    temp_date = a_tag.find("nobr", {"class": "eng list_vspace"}).get_text()
    temp_date = temp_date.replace("/", "-")
    current_day = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)

    if (":" in temp_date):
        temp_date = current_day + " " + temp_date

    print(temp_date)

    # latest_update < temp_date
    if (latest_update<temp_date):

        current_image = "http:" + a_tag.find("td", {"valign": "top"}).find("img")["src"]
        print(current_image)

        current_middle = a_tag.find("td", {"valign": "middle"})
        current_link = "http://www.ppomppu.co.kr/zboard/" + current_middle.find("a")["href"]

        content_url = current_link
        content_html = requests.get(content_url).text
        content_soup = BeautifulSoup(content_html, 'html.parser')

        goods_link=content_soup.find("div", {"class":"wordfix"}).find("a")["href"]
        print(goods_link)

        if (current_middle.find("font")):
            current_list_title = current_middle.find("font").get_text()

            price_index = current_list_title.rfind("(") + 1
            temp_string = current_list_title[price_index:]
            temp_index = temp_string.find("/")
            price_string = temp_string[:temp_index]

            print(temp_string[:temp_index] + "\n")

        else:
            current_list_title = current_middle.find("a").get_text()
            current_list_title = current_list_title.replace("<b>", "")
            current_list_title = current_list_title.replace("</b>", "")

            price_index = current_list_title.rfind("(") + 1
            temp_string = current_list_title[price_index:]
            temp_index = temp_string.find("/")
            price_string = temp_string[:temp_index]

            print(temp_string[:temp_index] + "\n")


if __name__ == '__main__':

    latest_update=check_latest_update()

    while(1):
        print("\n-체크-")

        url = 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu4&page_num=20&category=&search_type=sub_memo&keyword=%C4%B7%C7%CE'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        for a_tag in soup.select('.list0'):
            check_crawling_target(a_tag,latest_update)

        for a_tag in soup.select('.list1'):
            check_crawling_target(a_tag, latest_update)

        latest_update = check_latest_update()
        time.sleep(300)


