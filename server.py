from flask import Flask, render_template, request
from bs4 import BeautifulSoup, Tag
from parser import get_participants
import datetime

app = Flask(__name__)


def base_table(soup: BeautifulSoup) -> Tag:
    """
    Создание базовой таблицы (с заголовками)
    :param soup: soup на html страницу
    :return: базовая таблица
    """
    # Создаем таблицу
    table = soup.new_tag("table", border="1", cellspacing="0", cellpadding="10")

    # Создаем строку заголовков
    header_row = soup.new_tag("tr")

    # Добавляем заголовки в строку
    headers = ["№", "name", "weight", "y.o", "country", "region", "town"]
    for header in headers:
        th = soup.new_tag("td")
        th.string = header
        header_row.append(th)

    # Добавляем строку заголовков в таблицу
    table.append(header_row)

    # Добавляем таблицу в тело страницы
    return table


@app.route("/")
def main_menu():
    return render_template("index.html")


@app.route('/update', methods=['POST'])
def update_page():
    """Обновляет страницу по POST-запросу"""
    # Чтение HTML-файла
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_string = f.read()

    # Парсинг HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html_string, "html.parser")

    table = base_table(soup)

    url: str = request.form.get("url_nomination")
    if url:
        persons, status = get_participants(url)
        if status == "OK":
            for category, category_persons in persons.items():
                cells_category_row = soup.new_tag("tr")

                th = soup.new_tag("td")
                th.string = category
                if "девушки" in category.lower() or "юниорки" in category.lower() or "женщины" in category.lower():
                    color = "deeppink"
                elif "открытая" in category.lower() or "мастера" in category.lower():
                    color = "#ff7600"  # что-то оранжевое
                else:
                    color = "blue"
                th['style'] = f"color: {color}; font-weight: bold;"
                cells_category_row.append(soup.new_tag("td"))
                cells_category_row.append(th)
                table.append(cells_category_row)

                position: int = 1
                old_weight: str = ""
                for person in category_persons:
                    now_weight: str = person["weight"]
                    if now_weight != old_weight:
                        position = 1
                    cells_row = soup.new_tag("tr")
                    cells = [str(position),
                             person["name"],
                             now_weight,
                             str(datetime.date.today().year - int(person["birth_year"])),
                             person["country"],
                             person["region"],
                             person["town"]]
                    for cell in cells:
                        th = soup.new_tag("td")
                        th.string = cell
                        cells_row.append(th)

                    table.append(cells_row)
                    position += 1
                    old_weight = person["weight"]
            soup.body.append(table)
        else:
            new_p = soup.new_tag("p")
            new_p.string = status
            soup.body.append(new_p)
        # Возвращение измененного HTML
        return soup.prettify()
    else:
        new_p = soup.new_tag("p")
        new_p.string = "Void input"
        soup.body.append(new_p)
        return soup.prettify()


if __name__ == '__main__':
    app.run(debug=True)