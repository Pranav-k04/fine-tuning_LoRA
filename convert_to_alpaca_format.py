import json
import os

def convert_to_alpaca_format(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    alpaca_data = []
    for item in data:
        title = item.get("question_title", "").strip()
        body = item.get("question_body", "").strip()
        answer = item.get("answer", "").strip()

        # Combine title + body into single instruction
        instruction = f"{title}\n\n{body}".strip()

        alpaca_data.append({
            "instruction": instruction,
            "input": "",
            "output": answer
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(alpaca_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(alpaca_data)} samples → {output_path}")

if __name__ == "__main__":
    os.makedirs("data/alpaca", exist_ok=True)
    convert_to_alpaca_format("data/train.json", "data/alpaca/train_alpaca.json")
    convert_to_alpaca_format("data/test.json", "data/alpaca/test_alpaca.json")
