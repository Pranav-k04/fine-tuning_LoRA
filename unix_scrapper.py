import requests
import json
import time
import os
from tqdm import tqdm

API_URL = "https://api.stackexchange.com/2.3/questions"
SITE = "unix"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"} # Good practice to use a more complete user-agent

TAGS = [ "gzip", "venv"]
PAGES_PER_TAG = 3 # Be mindful of the total requests this generates (PAGES_PER_TAG * PAGE_SIZE * 2 requests per tag)
PAGE_SIZE = 20
SAVE_FILE = "data/qa_pairs.json"

# Global variable to track backoff time
GLOBAL_BACKOFF = 0

def make_api_request(url, params):
    global GLOBAL_BACKOFF
    retries = 0
    max_retries = 5
    while retries < max_retries:
        if GLOBAL_BACKOFF > 0:
            print(f"😴 Global backoff active. Sleeping for {GLOBAL_BACKOFF} seconds...")
            time.sleep(GLOBAL_BACKOFF)
            GLOBAL_BACKOFF = 0 # Reset after sleeping
        
        try:
            response = requests.get(url, params=params, headers=HEADERS)
            data = response.json()

            if "backoff" in data:
                # API explicitly tells us to backoff
                GLOBAL_BACKOFF = data["backoff"] + 1 # Add a buffer second
                print(f"🚦 API requested backoff: {data['backoff']} seconds. Setting global backoff.")
                time.sleep(GLOBAL_BACKOFF)
                GLOBAL_BACKOFF = 0 # Reset after sleeping
                continue # Retry the request after backoff

            if response.status_code == 429: # Too Many Requests
                wait_time = 2 ** retries # Exponential backoff
                print(f"⚠️ Received 429 (Too Many Requests). Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
                continue
            elif response.status_code != 200:
                print(f"⚠️ Non-200 status code: {response.status_code}. Response: {data}")
                return None # Or raise an error, depending on desired behavior

            return data

        except requests.exceptions.RequestException as e:
            wait_time = 2 ** retries
            print(f"❌ Network error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
            continue
        
    print(f"❌ Max retries reached for URL: {url} with params: {params}")
    return None

def fetch_questions(tag, page):
    params = {
        "order": "desc",
        "sort": "votes",
        "tagged": tag,
        "site": SITE,
        "filter": "withbody",
        "page": page,
        "pagesize": PAGE_SIZE
    }
    return make_api_request(API_URL, params)

def fetch_top_answer(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": SITE,
        "filter": "withbody"
    }
    data = make_api_request(url, params)
    if data and data.get("items"):
        return data["items"][0]["body"]
    return None

def save_progress(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    os.makedirs("data", exist_ok=True)
    all_qas = []

    # Resume from existing file if present
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            all_qas = json.load(f)
        print(f"🔄 Resuming from {len(all_qas)} existing Q&A pairs")

    for tag in TAGS:
        print(f"\n🔍 Tag: {tag}")
        for page in range(1, PAGES_PER_TAG + 1):
            print(f"  📄 Page {page}")
            questions_data = fetch_questions(tag, page)
            if not questions_data or not questions_data.get("items"):
                print(f"🚫 No questions found for tag {tag}, page {page} or API error occurred.")
                continue

            for item in tqdm(questions_data["items"], desc=f"{tag} Page {page}"):
                q_id = item["question_id"]
                
                # Check if this Q&A pair is already collected
                # This simple check assumes unique question_id or (question_title, question_body) combination
                # A more robust check might be needed for large datasets or complex resume logic
                is_duplicate = False
                for existing_qa in all_qas:
                    if existing_qa.get("question_title") == item["title"] and \
                       existing_qa.get("question_body") == item["body"]:
                        is_duplicate = True
                        break
                if is_duplicate:
                    # print(f"Skipping already collected QID: {q_id}")
                    continue

                q_title = item["title"]
                q_body = item["body"]
                a_body = fetch_top_answer(q_id) # This is a separate API call

                if a_body:
                    qa_pair = {
                        "question_title": q_title,
                        "question_body": q_body,
                        "answer": a_body,
                        "url": item["link"]
                    }
                    all_qas.append(qa_pair)
                    save_progress(all_qas)  # 💾 Save after each pair
                else:
                    print(f"Skipping QID {q_id} due to no answer or error fetching answer.")
                
                # Introduce a small, consistent delay between requests to be polite
                # and avoid hitting rate limits too quickly, in addition to backoff logic.
                time.sleep(0.5) 

    print(f"\n✅ Done! Total Q&A pairs collected: {len(all_qas)}")

if __name__ == "__main__":
    # If you got throttled for a long time, you might want to manually set GLOBAL_BACKOFF
    # before running main, or wait for the indicated time.
    # GLOBAL_BACKOFF = 84502 # Use this only if you know you're currently throttled for this duration.
    main()