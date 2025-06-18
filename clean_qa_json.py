import json
import os
from bs4 import BeautifulSoup
from bs4.element import NavigableString


def html_to_markdown_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Format <pre><code> as markdown fenced blocks
    for pre in soup.find_all("pre"):
        code = pre.get_text()
        fenced = f"\n```bash\n{code.strip()}\n```\n"
        pre.replace_with(NavigableString(fenced))

    # Format <blockquote> as > quoted text
    for block in soup.find_all("blockquote"):
        quote_lines = block.get_text().strip().splitlines()
        quoted = "\n".join(f"> {line.strip()}" for line in quote_lines if line.strip())
        block.replace_with(NavigableString(f"\n{quoted}\n"))

    # Get final plain markdown text
    return soup.get_text(separator="\n").strip()

def clean_json(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned_data = []

    for item in raw_data:
        cleaned_item = {
            "question_title": item["question_title"],
            "question_body": html_to_markdown_text(item["question_body"]),
            "answer": html_to_markdown_text(item["answer"]),
            "url": item["url"]
        }
        cleaned_data.append(cleaned_item)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved markdown-cleaned Q&A to {output_path}")

if __name__ == "__main__":
    clean_json("data/qa_pairs.json", "data/qa_cleaned.json")
