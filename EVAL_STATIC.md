these are the Evaluation metrics after fine-tuning the model (find these results in tinyLlama.ipynb)
🔍 Generating predictions for base and fine-tuned models...



📋 Evaluation Table (Manual Scoring):

| # | Prompt | Base Output (truncated) | Fine-Tuned Output (truncated) | Plan Score |
|---|--------|--------------------------|-------------------------------|-------------|
| 1 | Remove files from tar archive  I ha... | I don't have the capability to run a com... | I don't have the capability to run a com... | 2 |
| 2 | Display only relevant hunks of a di... | I'm not sure if I'm asking the right que... | I'm not sure if I'm asking the right que... | 2 |
| 3 | Why use superflous dash (-) to pass... | The reason is that the tar command is a ... | The reason is that the tar command is a ... | 2 |
| 4 | Why is less being run unnecessarily... | ... | ... | 0 |
| 5 | How to keep track of changes in /et... | ... | ... | 0 |
| 6 | How do I recursively delete all `.t... | ``` #!/bin/bash  # Recursively delete al... | ``` #!/bin/bash  # Recursively delete al... |2 |
| 7 | What happens if I run `rm -rf /` wi... | ... | ... | 0 |


📈 Metrics Evaluation
ROUGE: {'rouge1': 0.20529351883271124, 'rouge2': 0.15038750032783446, 'rougeL': 0.1901804199940846, 'rougeLsum': 0.19349304939367049}
BLEU : {'bleu': 0.28887377670764713, 'precisions': [0.39076154806491886, 0.27478042659974905, 0.2610340479192938, 0.2572877059569075], 'brevity_penalty': 0.9912989985778248, 'length_ratio': 0.9913366336633663, 'translation_length': 801, 'reference_length': 808}
