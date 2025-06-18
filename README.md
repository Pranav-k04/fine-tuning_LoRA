# fine-tuning_LoRA
# 🦙 TinyLlama Bash/Git Q&A Agent

This project fine-tunes [TinyLlama-1.1B-Chat](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) using real Q&A data from Unix StackExchange to create a lightweight command-line assistant for Bash, Git, tar/gzip, grep, and virtual environments.

---

## 📦 Project Structure

├── data/ # Cleaned Alpaca-style JSON datasets
├── merged-tinyllama/ # Final model after merging LoRA
├── tinyllama-cli-lora/ # LoRA adapter files (for training)
├── agent.py # CLI assistant (torch-free inference)
├── training.ipynb / .py # End-to-end training script
├── eval_static.md # Base vs FT + BLEU/ROUGE + scores
├── eval_dynamic.md # Agent runs + plan score table
├── report.md # One-page project summary
├── requirements.txt
└── README.md # You are here


---

## 🧠 What It Does

- Learns to answer technical Bash/Git questions
- Fine-tunes TinyLlama using Q&A pairs scraped from Unix StackExchange
- Builds a low-memory CLI assistant that works on CPU/GPU
- Supports BLEU/ROUGE evaluation + plan scoring

---

## 🚀 Setup Instructions

### 1. 🧼 Install Dependencies

```bash
pip install -r requirements.txt
```

run these python scripts to collect and clean data but since it's already uploded 
ignore this step 
```
python stack_scraper.py
python clean_to_alpaca.py
```
### 2 fine-tune-tinyLlama

run the tinyLlama.ipynb to create download adapter files and model from hugging face 
also train the model on the data and save checkpoint.
PS if not able to downlaod the model and re-train it find my pretrained saved model here : 
### 3 Run Agent.py 
Use Cli to load and querry with tinyLlama 
example 
```
python agent.py "How to create and switch to a new Git branch?"
```
