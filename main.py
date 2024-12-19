import requests
from bs4 import BeautifulSoup


def print_links(soup: BeautifulSoup):
    a_links = soup.select("a")

    for link in a_links:
        print(link.get_text())


def get_participants(soup: BeautifulSoup):
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
            country, area, town = info[1][2].split(",")[0:3]
            info_dict["country"] = country
            info_dict["area"] = area[1:]
            info_dict["town"] = town
            names[now_group].append(info_dict)
    return names


print("Получение ответа от powertable.ru...")
url = "https://powertable.ru/api/hs/p/nomination?nom=2727&lg=&dsp=0675"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

persons = get_participants(soup)
for person in persons["Мужчины"]:
    print(person)
    print("Получение ответа от allpowerlifting.com...")
    base_url_all_pl = "https://allpowerlifting.com/lifters/"
    url_all_pl = (
        base_url_all_pl
        + f"?name={person["name"].replace(" ", "+")}&birth_year={person["birth_year"]}&gender=&search="
    )
    print(url_all_pl)
    response = requests.get(url_all_pl)
    print(response.text)
    break

# for group, nnn in names.items():
#     print(f"---Group: {group}---")
#     for name in nnn:
#         for parameter in name.values():
#             print(parameter, end=", ")
#         print()
