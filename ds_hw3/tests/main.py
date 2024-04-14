from datetime import datetime
import json
import re
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://index.minfin.com.ua/ua/russian-invading/casualties"


def get_urls():
    urls = ["/"]
    html_doc = requests.get(BASE_URL)
    soup = BeautifulSoup(html_doc.content, features="html.parser")
    content = soup.select("div[class=ajaxmonth] h4[class=normal] a")
    prefix = "/month.php?month="  # month.php?month=2023-09
    for link in content:
        url = (
            prefix + re.search(pattern=r"\d{4}-\d{2}", string=link["id"]).group()
        )  # 2023-09
        urls.append(url)
    return urls


def spider(url):
    result = []
    html_doc = requests.get(BASE_URL + url)
    soup = BeautifulSoup(html_doc.content, features="html.parser")
    content = soup.select("ul[class=see-also] li[class=gold]")
    for li in content:
        parse_elements = {}
        date_key = li.find(name="span", attrs={"class": "black"}).text
        try:
            date_key = datetime.strptime(date_key, "%d.%m.%Y").isoformat()
        except ValueError:
            print(f"ERROR for {date_key}")
            continue
        parse_elements.update({"date": date_key})
        casualties = li.find("div").find("div").find("ul")
        for casualt in casualties:
            name, quantity, *_ = casualt.text.split("—")
            name = name.strip()
            quantity = re.search(pattern=r"\d+", string=quantity).group()
            parse_elements.update({name: quantity})
        result.append(parse_elements)
    return result


def main(urls):
    data = []
    for url in urls:
        data.extend(spider(url))
    return data


if __name__ == "__main__":
    print(result := main(get_urls()))
    with open('kacapy.json','w',encoding='utf-8') as fd:
        json.dump(result,fd,ensure_ascii=False,indent=4)

 