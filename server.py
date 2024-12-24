from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from parser import get_participants
from typing import Dict, List

app = Flask(__name__)


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

    url: str = request.form.get("url_nomination")
    if url:
        persons: Dict[str, List[Dict[str, str]]] = get_participants(url)

        for person in persons["Мужчины"]:
            new_p = soup.new_tag("p")
            new_p.string = person["name"]
            soup.body.append(new_p)

        # Возвращение измененного HTML
        return soup.prettify()
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)