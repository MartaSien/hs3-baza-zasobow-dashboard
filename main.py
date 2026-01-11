DISCOURSE_URL = "https://kb.hs3.pl/" # Database is hosted here
DISCOURSE_CATEGORY = 9 # Database is stored in this Discourse category

from discourse import Discourse

if __name__ == "__main__":
    print(f"Discourse database: f{DISCOURSE_URL}/{DISCOURSE_CATEGORY}")
    print("Fetching database data to zasoby.csv...")
    dis = Discourse(DISCOURSE_URL)
    
    print("Generating HTML dashboard...")
    print("Done!")