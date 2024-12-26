import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Tuple


BASE_URL_ALL_PL: str = "https://allpowerlifting.com"


def get_all_athletes(person: Dict[str, str]) -> List[List[str]]:
    """
    Получить список всех спортсменов, имеющих такое же имя, фамилию и год рождения как у person
    :param person: словарь данных о спортсмене (имя, вес, город, дата рождения и т.д.)
    :return: список найденных спортсменов
    """
    # Формирование ссылки на страницу с найденными атлетами
    url_all_pl = (
            BASE_URL_ALL_PL
            + f"/lifters/?name={person["name"].replace(" ", "+")}&birth_year=&gender=&search="
    )

    print(f"Получение ответа от {url_all_pl}...")
    response = requests.get(url_all_pl)

    soup = BeautifulSoup(response.text, "html.parser")
    tr_elements = soup.select("tr")
    find: List[List[str]] = []
    for tr in tr_elements:
        # Split данных из табл. в список. (ID, пол, имя, откуда, год рождения, выступления, рекорды, медиа, кто добавил)
        info: List[str] = re.split(r"[\n ]+", tr.get_text())
        if info[6] == person["birth_year"]:  # Проверка на совпадение возраста
            href = tr.select("a")[0].get("href")  # Получение ссылки на спортсмена
            info.append(href)  # Добавление ссылки в общий список информации о спортсмене
            find.append(info)  # Добавление найденного спортсмена, подходящего по дате рождения
    return find


def get_best_results(url_athlete: str):
    response = requests.get(url_athlete)  # Получение личной страницы спортсмена на allpl
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select('td.text-center span.text-success')
    best_results = []
    for result in results:
        best_results.append(float(result.get_text().replace(",", ".")))
    return best_results


def allPowerlifting(person: Dict[str, str]) -> Dict[str, str]:
    """
    Получить данные, рекорды спортсменов с сайта allpowerlifting.com
    :param person: словарь, описывающий данные спортсмена (имя, вес, город, дата рождения и т.д.)
    :return: объект person, дополненный рекордами
    """
    find: List[List[str]] = get_all_athletes(person)

    if len(find) > 0:
        href = find[0][-1]
        best_results = get_best_results(BASE_URL_ALL_PL + href)
        person["results"] = str(best_results)
    return person


def print_links(soup: BeautifulSoup):
    a_links = soup.select("a")

    for link in a_links:
        print(link.get_text())


def get_participants(url: str) -> Tuple[Dict[str, List[Dict[str, str]]], str]:
    """
    Получить список участников из номинации с сайта powertable.ru
    :param url: url страницы номинации
    :return: кортеж, содержащий статус выполнения и словарь участников {'Мужчины': [{'name': 'Борух Сергей',
    'birth_year': '1988', 'weight': '82,5', 'country': 'Россия', 'region': 'Оренбургская область', 'town': 'Сорочинск'},
    ...]}
    """
    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema:
        return {}, "Invalid URL"
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
    return names, "OK"


if __name__ == '__main__':
    # print("Получение ответа от powertable.ru...")
    # Aurl = "https://powertable.ru/api/hs/p/nomination?nom=3091&lg=&dsp=0307"  # "https://powertable.ru/api/hs/p/nomination?nom=2727&lg=&dsp=0675"
    #
    # Apersons, Astatus = get_participants(Aurl)
    # print(Apersons)
    # for Acategory, Acategory_persons in Apersons.items():
    #     print("---", Acategory)
    #     for Aperson in Acategory_persons:
    #         print(Aperson)
    print(get_best_results("https://allpowerlifting.com/lifters/RUS/ryzhov-artem-227356"))