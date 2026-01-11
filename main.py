DISCOURSE_URL = "https://kb.hs3.pl/" # Database is hosted here
DISCOURSE_CATEGORY = 9 # Database is stored in this Discourse category

import os, shutil
from jinja2 import Environment, FileSystemLoader
import pandas as pd

from discourse import Discourse

def generate_dashboard():
    """Generate dashboard from zasoby.csv file"""
    website_folder = "docs"
    data = pd.read_csv("zasoby.csv")
    env = Environment(loader=FileSystemLoader("template"))
    
    shutil.rmtree(f"./{website_folder}")
    os.mkdir(f"./{website_folder}")
    shutil.copytree("template/static", f"{website_folder}/static")
    
    print("Creating page to static file.")
    template = env.get_template("_main_layout.html")
    with open(f"{website_folder}/index.html", "w+", encoding="utf-8") as file:
        header_row = data.columns.values.tolist()
        rows = data.values.tolist()
        html = template.render(title="Baza Zasobów Hackerspace Trójmiasto", t_header=header_row, t_body=rows)
        file.write(html)


if __name__ == "__main__":
    print(f"Discourse database: {DISCOURSE_URL}{DISCOURSE_CATEGORY}")
    print("Fetching database data to zasoby.csv")
    dis = Discourse(DISCOURSE_URL)
    dis.category_topics_csv(DISCOURSE_CATEGORY)
    print("Generating HTML dashboard")
    generate_dashboard()
    print("Done!")