from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_info(id):
    url = "https://www.kare-design.com/shop/ua/ru/query/" + id

    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    div = soup.find(attrs={"class", "facts"})
    ps = div.findAll("p")

    desc = ps[0].contents[0] + "\n"
    tech = parse_ps(ps[1:])

    return desc + "\n" + tech


def parse_list(list):
    result = ""
    for li in list.findAll("li"):
        result += li.getText() + ".\n"
    return result


def parse_ps(ps):
    result = ""
    for p in ps:
        if not p.getText().__contains__("Скачать"):
            result += p.getText() + "\n"
    return result






