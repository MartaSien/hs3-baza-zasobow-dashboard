import os, re, shutil
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from discourse import DiscourseDatabase


def add_download_button(row):
    item_id = re.sub(r'<a href.*/([0-9]+)".*', "\\1", row[1])
    download_button = (
        f'<button id="btn_{item_id}"><i class="fa fa-download"></i> {item_id}</button>'
    )
    return row + [download_button]


def generate_dashboard():
    """Generate dashboard from zasoby.csv file"""
    print("Generating HTML dashboard")
    website_folder = "docs"
    data = pd.read_csv("zasoby.csv")
    env = Environment(loader=FileSystemLoader("template"))
    print("Removing old website files")
    shutil.rmtree(f"./{website_folder}")
    os.mkdir(f"./{website_folder}")
    print("Creating a new website")
    shutil.copytree("template/static", f"{website_folder}/static")
    template = env.get_template("_main_layout.html")
    with open(f"{website_folder}/index.html", "w+", encoding="utf-8") as file:
        header_row = data.columns.values.tolist() + ["label"]
        rows = map(
            add_download_button,
            data.values.tolist(),
        )
        html = template.render(
            title="Baza Zasobów Hackerspace Trójmiasto",
            t_header=header_row,
            t_body=rows,
        )
        file.write(html)


if __name__ == "__main__":
    DiscourseDatabase()
    generate_dashboard()
    print("Done!")

