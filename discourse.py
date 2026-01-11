'''
Class to generate a csv file based on data fetched via Discourse REST API
'''
import requests
import json

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

    def get_category_topics(self, category_id: str) -> requests.Response:
        """Get topics from a Discourse category"""
        cat_data = self.get_category_data(category_id)
        for topic in cat_data["topic_list"]["topics"]:
            print(f'{topic["id"]}, {topic["title"]}, {topic["tags"]}, {self.url}t/{topic["id"]}')

    
if __name__=="__main__":
    dis = Discourse("https://kb.hs3.pl/")
    dis.get_category_topics(9)
