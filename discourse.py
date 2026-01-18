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
        load_dotenv()
    
    def get_headers(self, auth=False):
        """Get request headers, optionally with auth data."""
        headers = {
            "content-type": "application/json",
        }
        if auth:
            headers["Api-Key"] = os.getenv("DISCOURSE_PAT")
            headers["Api-Username"] = os.getenv("DISCOURSE_USERNAME")
        return headers

    def get_category_data(self) -> dict:
        """Get all topics from a Discourse category with pagination"""
        url = f"{DISCOURSE_URL}/c/{CATEGORY_ID}.json"
        print(f"Fetching data from {url}")
        all_topics = []
        page = 0
        while True:
            params = {"per_page": 100, "page": page}
            res = requests.get(url, headers=self.get_headers(), params=params)
            res.raise_for_status()
            res_json = res.json()
            topics = res_json["topic_list"]["topics"]
            if not topics:
                break
            for topic in topics:
                if topic["category_id"] == CATEGORY_ID:
                    all_topics.append(topic)
            print(f"Fetched page {page}: {len(topics)} topics, {len(all_topics)} total in category")
            page += 1
        return {"topic_list": {"topics": all_topics}}
    
    def get_topic_content(self, topic_id: str):
        """Get a single topic's content"""
        get_url = f"{DISCOURSE_URL}/posts/{topic_id}.json"
        res = requests.get(get_url, headers=self.get_headers(auth=True))
        res.raise_for_status()
        return res.json()

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