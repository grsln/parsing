import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 '
                  'Safari/537.36 '
}

url = 'https://zakupki.gov.ru/epz/rkpo/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1' \
      '%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10' \
      '&sortBy=UPDATE_DATE&active=on&region_selectedSubjects_21959484=region_selectedSubjects_21959484' \
      '&region_selectedSubjects_21959485=region_selectedSubjects_21959485&region_selectedSubjects_21959486' \
      '=region_selectedSubjects_21959486&region_selectedSubjects_21959487=region_selectedSubjects_21959487' \
      '&region_selectedSubjects_21959488=region_selectedSubjects_21959488&region_selectedSubjects_21959489' \
      '=region_selectedSubjects_21959489&region_selectedSubjects_21959490=region_selectedSubjects_21959490' \
      '&region_selectedSubjects_21959491=region_selectedSubjects_21959491&region_selectedSubjects_27517303' \
      '=region_selectedSubjects_27517303&region_selectedSubjects_30322762=region_selectedSubjects_30322762' \
      '&selectedSubjects=21959484%2C21959485%2C21959486%2C21959487%2C21959488%2C21959489%2C21959490%2C21959491' \
      '%2C27517303%2C30322762&customerPlaceWithNested=on '
urls = []
base_url = 'https://zakupki.gov.ru'
session = requests.Session()
r = session.get(url, headers=headers)
# ---------------------------------ПОИСК СТРАНИЦ
if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'lxml')
    try:
        pagination = soup.find_all('a', attrs={'class': 'page__link'})
        # count = int(pagination[-1].text)
        # print(count)
        count = 2
        for i in range(count):
            url = f'https://zakupki.gov.ru/epz/rkpo/search/results.html?morphology=on&' \
                  f'search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&' \
                  f'pageNumber={i}&sortDirection=false&recordsPerPage=_10&sortBy=UPDATE_DATE&active=on&' \
                  f'region_selectedSubjects_21959484=region_selectedSubjects_21959484&region_selectedSubjects_21959485=' \
                  f'region_selectedSubjects_21959485&region_selectedSubjects_21959486=region_selectedSubjects_21959486&' \
                  f'region_selectedSubjects_21959487=region_selectedSubjects_21959487&region_selectedSubjects_21959488=' \
                  f'region_selectedSubjects_21959488&region_selectedSubjects_21959489=region_selectedSubjects_21959489&' \
                  f'region_selectedSubjects_21959490=region_selectedSubjects_21959490&region_selectedSubjects_21959491=' \
                  f'region_selectedSubjects_21959491&region_selectedSubjects_27517303=region_selectedSubjects_27517303&' \
                  f'region_selectedSubjects_30322762=region_selectedSubjects_30322762&selectedSubjects=21959484%2C21959' \
                  f'485%2C21959486%2C21959487%2C21959488%2C21959489%2C21959490%2C21959491%2C27517303%2C30322762&' \
                  f'customerPlaceWithNested=on'
            if url not in urls:
                urls.append(url)
    except:
        pass
    # print(urls)
    requirm = ['Название', 'Сокращенное наименование', 'ИНН', 'Адрес электронной почты',
               'Лицо, имеющее право действовать без доверенности от имени юридического лица',
               'Контактные телефоны']
    # ---------------------------------ПЕРЕБОР СТРАНИЦ
    data = []
    for url in urls:
        r = session.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'row no-gutters registry-entry__form mr-0'})
        # ---------------------------------ВХОД В ПОДСТРАНИЦЫ
        for div in divs:
            title = div.find('div', attrs={'class': 'registry-entry__body-href'}).text
            href = base_url + div.find('a', attrs={'class': 'text-uppercase'})['href']
            r2 = session.get(href, headers=headers)
            soup2 = BeautifulSoup(r2.content, 'lxml')
            # ---------------------------------ПОИСК В ПОДСТРАНИЦЕ
            sub_divs = soup2.find_all('div', attrs={'class': 'blockInfo__section'})
            sub_data = {}
            # sub_data = []
            sub_data['Название'] = ' '.join(title.split())
            for sub_div in sub_divs:
                sections = sub_div.find_all('section', attrs={'class': 'blockInfo__section section'})
                for section in sections:
                    title_section = section.find('span', attrs={'class': 'section__title'}).text
                    info_section = section.find('span', attrs={'class': 'section__info'}).text
                    if (' '.join(title_section.split())) in requirm:
                        # sub_data.append(' '.join(title_section.split()))
                        # sub_data.append(' '.join(info_section.split()))
                        print(' '.join(title_section.split()))
                        sub_data[' '.join(title_section.split())] = ' '.join(info_section.split())

            data.append(sub_data)
            print(sub_data)
            # print(' '.join(sub_div.text.split()))
    for i in data:
        print(i)
    with open('data.csv', 'w', newline='') as file_csv:
        a_pen = csv.writer(file_csv, quoting=csv.QUOTE_NONNUMERIC)
        # a_pen.writerows(data)
        a_pen.writerow(data[0])
        for x in data:
            a_pen.writerow(x.values())
