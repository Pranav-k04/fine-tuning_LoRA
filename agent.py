import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.pipelines import pipeline

# === Config ===
MODEL_PATH = "./merged-tinyllama"

# === Load model and tokenizer ===
def load_model():
    print("📦 Loading model and tokenizer from", MODEL_PATH)
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float16 if torch.cuda.is_available() else None
        )
        return model, tokenizer
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)

# === Generate response from prompt ===
def generate_response(model, tokenizer, prompt):
    if not prompt.strip():
        return "❗ Empty prompt received."

    device = 0 if torch.cuda.is_available() else -1
    print(f"🚀 Running on {'GPU' if device == 0 else 'CPU'}")

    full_prompt = f"### Instruction:\n{prompt.strip()}\n\n### Response:\n"
    try:
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)
        outputs = pipe(full_prompt, max_new_tokens=128, pad_token_id=tokenizer.eos_token_id)

        if outputs and isinstance(outputs, list):
            response = outputs[0].get("generated_text", "")
            return response.split("### Response:")[-1].strip()
        else:
            return "❗ No output generated."
    except Exception as e:
        return f"❌ Inference failed: {e}"

# === Entry point ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Usage: python agent.py \"Your instruction prompt here\"")
        sys.exit(1)

    user_prompt = sys.argv[1]
    model, tokenizer = load_model()
    response = generate_response(model, tokenizer, user_prompt)

    print("\n🧠 Response:")
    print(response)
