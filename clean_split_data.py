import json
import os
import random
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

def html_to_text_fixed(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Replace each <kbd> with its text content
    for kbd in soup.find_all("kbd"):
        kbd.replace_with(NavigableString(kbd.get_text(strip=True)))

    # Join consecutive <kbd> elements with " + "
    for element in soup.find_all(["p", "li"]):
        if isinstance(element, Tag):  # 🛠 Ensure it's a Tag before calling .find_all()
            kbd_sequence = element.find_all("kbd")
            if len(kbd_sequence) > 1:
                combined = " + ".join(k.get_text(strip=True) for k in kbd_sequence)
                for k in kbd_sequence:
                    k.extract()
                element.insert(0, NavigableString(combined + " "))

    # Replace <pre> with markdown code blocks
    for pre in soup.find_all("pre"):
        code = pre.get_text()
        pre.replace_with(NavigableString(f"\n```bash\n{code.strip()}\n```\n"))

    # Convert blockquotes to markdown > quotes
    for block in soup.find_all("blockquote"):
        quote_lines = block.get_text().strip().splitlines()
        quoted = "\n".join(f"> {line.strip()}" for line in quote_lines if line.strip())
        block.replace_with(NavigableString(f"\n{quoted}\n"))

    return soup.get_text(separator="\n").strip()

def clean_and_split(input_path, output_dir, train_ratio=0.9):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    for item in data:
        cleaned.append({
            "question_title": item["question_title"],
            "question_body": html_to_text_fixed(item["question_body"]),
            "answer": html_to_text_fixed(item["answer"]),
            "url": item["url"]
        })

    random.shuffle(cleaned)
    split_idx = int(len(cleaned) * train_ratio)
    train_data = cleaned[:split_idx]
    test_data = cleaned[split_idx:]

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "train.json"), "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)

    with open(os.path.join(output_dir, "test.json"), "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Cleaned and split into {len(train_data)} train and {len(test_data)} test samples.")

if __name__ == "__main__":
    clean_and_split("data/qa_pairs.json", "data/")
