'''
Class to generate a csv file based on data fetched via Discourse REST API
'''
import requests
import json
import csv


DISCOURSE_URL = "https://kb.hs3.pl" # Database is hosted here
CATEGORY_ID = 9 # Database category ID

class DiscourseDatabase():
    def __init__(self):
        data = self.get_category_data()
        self.category_topics_csv(data)

    def get_category_data(self) -> requests.Response:
        """Get data from a Discourse category"""
        headers = {
            "content-type": "application/json",
        }
        url = f"{DISCOURSE_URL}/c/{CATEGORY_ID}.json"
        print(f"Fetching data from {url}")
        res = requests.get(url, headers)
        res.raise_for_status()
        res_json = json.loads(res.text)
        return res_json

    def category_topics_csv(self, category_data) -> None:
        """Save category topics to a csv file"""
        columns = ["id", "title", "place", "tags"]
        records = category_data["topic_list"]["topics"]
        with open('zasoby.csv', 'w', encoding='UTF8') as f:
            write = csv.writer(f)
            write.writerow(columns)
            for topic in records:
                html_url = f'<a href="{DISCOURSE_URL}/t/{topic["id"]}">{topic["title"]}</a>'
                place = self.get_place(topic)
                write.writerow([topic["id"], html_url, place, topic["tags"]])
        print(f"New zasoby.csv generated with {len(records)} records")

    def get_place(self, topic):
        """Get place of a topic"""
        places = ["cow-work", "garage", "lab"]
        for place in places:
            if place in topic["tags"]:
                return f'<a href="https://kb.hs3.pl/tag/{place}">{place}</a>'
        return "unknown"