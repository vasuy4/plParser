import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List


def allPowerlifting(persons: dict) -> None:
    """
    Получить данные, рекорды спортсменов с сайта allpowerlifting.com
    :param persons: словарь, полученный из функции get_participants
    :return:
    """
    for person in persons["Мужчины"]:
        base_url_all_pl = "https://allpowerlifting.com"
        url_all_pl = (
                base_url_all_pl
                + f"/lifters/?name={person["name"].replace(" ", "+")}&birth_year=&gender=&search="
        )
        print(f"Получение ответа от {url_all_pl}...")
        response = requests.get(url_all_pl)

        soup = BeautifulSoup(response.text, "html.parser")
        tr_elements = soup.select("tr")
        find = []
        for tr in tr_elements:
            info = re.split(r"[\n ]+", tr.get_text())
            if info[6] == person["birth_year"]:
                href = tr.select("a")[0].get("href")
                info.append(href)
                find.append(info)
        # print(find)

        if len(find) > 0:
            href = find[0][-1]
            url_profile = base_url_all_pl + href
            response = requests.get(url_profile)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.select('td.text-center span.text-success')
            best_results = []
            for result in results:
                best_results.append(float(result.get_text().replace(",", ".")))
            person["results"] = best_results
            print(person)


def print_links(soup: BeautifulSoup):
    a_links = soup.select("a")

    for link in a_links:
        print(link.get_text())


def get_participants(url: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Получить список участников из номинации с сайта powertable.ru
    :param url: url страницы номинации
    :return: словарь участников {'Мужчины': [{'name': 'Борух Сергей', 'birth_year': '1988', 'weight': '82,5', 'country':
    'Россия', 'region': 'Оренбургская область', 'town': 'Сорочинск'}, ...]}
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tr = soup.select("tr.const_c, tr.group_l")
    names = {}
    now_group = ""
    for name in tr:
        text = name.get_text()

        if text[0].isalpha():
            now_group = text
            names[now_group] = list()
        else:
            info = text.split("\n\n\n\n")
            info[1] = info[1].split("\n")[0:3]
            namee, birth_year = info[1][0].split(", ")
            if int(birth_year[0]) < 5:
                birth_year = "20" + birth_year
            else:
                birth_year = "19" + birth_year
            info_dict = {}
            info_dict["name"] = namee
            info_dict["birth_year"] = birth_year
            info_dict["weight"] = info[1][1]
            country, region, town = info[1][2].split(",")[0:3]
            info_dict["country"] = country
            info_dict["region"] = region[1:]
            info_dict["town"] = town
            names[now_group].append(info_dict)
    return names


# print("Получение ответа от powertable.ru...")
# url = "https://powertable.ru/api/hs/p/nomination?nom=3226&list=&lg="  # "https://powertable.ru/api/hs/p/nomination?nom=2727&lg=&dsp=0675"
# response = requests.get(url)
#
# soup = BeautifulSoup(response.text, "html.parser")
#
# persons = get_participants(soup)
# print(persons)
# for person in persons["Мужчины"]:
#     print(person)
