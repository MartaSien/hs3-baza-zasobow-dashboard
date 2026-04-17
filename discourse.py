'''
Class to generate a csv file based on data fetched via Discourse REST API
'''
import os
import csv
import json
import requests
import time
from dotenv import load_dotenv

DISCOURSE_URL = "https://kb.hs3.pl" # Database is hosted here
DATABASE_CAT_ID = 9 # Database category ID
PLACES = [
    "online",
    "cow-work",
    "garage",
    "lab",
    "audiolab",
    "server-room"
]
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

    def get_category_data(self, category_id = DATABASE_CAT_ID) -> dict:
        """Get all topics from a Discourse category with pagination"""
        url = f"{DISCOURSE_URL}/c/{category_id}.json"
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
                if topic["category_id"] == category_id:
                    all_topics.append(topic)
            print(f"Fetched page {page}: {len(topics)} topics, {len(all_topics)} total in category")
            page += 1
        return {"topic_list": {"topics": all_topics}}

    def get_first_post_id(self, topic_id: str):
        """Get the first post ID from the topic"""
        topic_url = f"{DISCOURSE_URL}/t/{topic_id}.json"
        topic_res = requests.get(topic_url, headers=self.get_headers(auth=True))
        topic_res.raise_for_status()
        topic_data = topic_res.json()
        return topic_data["post_stream"]["posts"][0]["id"]

    def get_post_contents(self, post_id: str):
        """Get content of the post"""
        post_url = f"{DISCOURSE_URL}/posts/{post_id}.json"
        post_res = requests.get(post_url, headers=self.get_headers(auth=True))
        post_res.raise_for_status()
        return post_res.json()

    def replace_post_content(self, post_id, new_content: str):
        """Replace post's content"""
        post_url = f"{DISCOURSE_URL}/posts/{post_id}.json"
        payload = {"post": {"raw": new_content}}
        res = requests.put(post_url, json=payload, headers=self.get_headers(auth=True))
        res.raise_for_status()
        return res.json()

    def put_tags(self, topic_id: str, tags: list):
        """Put tags to a topic"""
        url = f"{DISCOURSE_URL}/t/{topic_id}.json"
        payload = {"tags": tags}
        res = requests.put(url, json=payload, headers=self.get_headers(auth=True))
        res.raise_for_status()
        print(f"Added {tags} to {url}")

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
        for place in PLACES:
            if place in topic["tags"]:
                return f'<a href="https://kb.hs3.pl/tag/{place}">{place}</a>'
        return "unknown"

    def sync_places_tags(self, topic):
        """Update places tags, based on post's content"""
        new_tag_set = set(topic["tags"])
        post_id = self.get_first_post_id(topic["id"])
        content = self.get_post_contents(post_id)
        try:
            content_place = content["raw"].split("Miejsce zamieszkania")[1].split("|")[1]
        except:
            print("Place not found within the post!")
            return
        for place in PLACES:
            if content_place.lower().count(f"[{place}]"):
                new_tag_set.add(place)
        new_tag_list = list(new_tag_set)
        if sorted(topic["tags"]) != sorted(new_tag_list):
            self.put_tags(topic["id"], new_tag_list)

    def replace_string_in_post(self, topic_id: str, old_string: str, new_string: str) -> dict:
        """Replace a selected string within a topic's first post using Discourse REST API"""
        post_id = self.get_first_post_id(topic_id)
        old_post_data = self.get_post_contents(post_id)
        new_post_data = old_post_data["raw"].replace(old_string, new_string)
        return self.replace_post_content(post_id, new_post_data)

    
if __name__ == "__main__":
    disc = DiscourseDatabase()
    category = disc.get_category_data()
    records = category["topic_list"]["topics"]
    record_num = len(records)
    for i, topic in enumerate(records):
        print(f"{i}/{record_num}")
        disc.sync_places_tags(topic)
        if i%30 == 29:
            print("Wait 60s to avoid hitting the request limit.")
            time.sleep(60)
    """
    # Useful when tag name changes
    for topic in records:
        if "lab" in topic["tags"]:
            disc.replace_string_in_post(topic["id"], "[Workshop](https://kb.s.hs3.pl/tag/workshop)", "[Lab](https://kb.s.hs3.pl/tag/lab)")
    """