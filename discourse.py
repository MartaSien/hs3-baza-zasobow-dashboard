'''
Class to generate a csv file based on data fetched via Discourse REST API
'''
import requests
import json
import csv

class Discourse():
    def __init__(self, url):
        self.url = url

    def get_category_data(self, category_id: str) -> requests.Response:
        """Get data related to a Discourse category"""
        headers = {
            "content-type": "application/json",
        }
        url = f"{self.url}/c/{category_id}.json"
        res = requests.get(url, headers)
        res.raise_for_status()

        res_json = json.loads(res.text)
        return res_json

    def category_topics_csv(self, category_id: str) -> requests.Response:
        """Save category topics to a csv file"""
        cat_data = self.get_category_data(category_id)
        columns = ["id", "title", "tags"]
        with open('zasoby.csv', 'w', encoding='UTF8') as f:
            write = csv.writer(f)
            write.writerow(columns)
            for topic in cat_data["topic_list"]["topics"]:
                html_url = f'<a href="{self.url}t/{topic["id"]}">{topic["title"]}</a>'
                write.writerow([topic["id"], html_url, topic["tags"]])
