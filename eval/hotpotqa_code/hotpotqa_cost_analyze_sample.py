import pandas as pd
from datasets import load_dataset
import tiktoken
import numpy as np

# --- Configuration ---
SAMPLE_SIZE = 300
SEED = 42  # Using a fixed seed ensures we get the same "random" sample every time
OUTPUT_FILENAME = f"hotpotqa_sample_{SAMPLE_SIZE}_analysis.csv"

# --- Model Pricing (per 1,000,000 tokens) ---
# NOTE: Prices are based on standard models as of mid-2024 and can change.
# Always check the official OpenAI pricing page for the latest numbers.
MODEL_PRICING = {
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-4":           {"input": 30.00, "output": 60.00}, # Standard gpt-4 is more expensive
    "gpt-4-turbo":     {"input": 10.00, "output": 30.00},
    "gpt-4o":          {"input": 5.00, "output": 15.00},
    "gpt-4o-mini":     {"input": 0.15, "output": 0.60},
}


# 1. Load the dataset and create a reproducible sample
print(f"Loading HotpotQA dataset and creating a reproducible sample of {SAMPLE_SIZE} items...")
ds = load_dataset("hotpot_qa", "fullwiki")
# .shuffle(seed=...) is the key to getting the same random sample every time.
# .select(range(...)) takes the first N items from that shuffled set.
train_sample = ds["train"].shuffle(seed=SEED).select(range(SAMPLE_SIZE))
print(f"Sample of {len(train_sample)} examples created successfully.")


# 2. Initialize the tokenizer
# "cl100k_base" is the correct encoding for all specified models.
try:
    encoding = tiktoken.get_encoding("cl100k_base")
except Exception:
    encoding = tiktoken.encoding_for_model("gpt-4")


# 3. Process ONLY the sample to count input and output tokens
results = []
print(f"Analyzing {SAMPLE_SIZE} samples to calculate token counts...")

for idx, item in enumerate(train_sample):
    # --- Calculate Input Tokens ---
    context_titles = " ".join(item['context']['title'])
    context_sentences = " ".join(sum(item['context']['sentences'], []))
    full_context = context_titles + " " + context_sentences
    question = item['question']
    input_prompt = f"Context: {full_context}\n\nQuestion: {question}"
    input_tokens = len(encoding.encode(input_prompt))
    
    # --- Calculate Output Tokens ---
    # The output is the ground-truth answer
    answer = item['answer']
    output_tokens = len(encoding.encode(answer))
    
    results.append({
        "SampleID": idx,
        "QuestionID": item['id'],
        "Question": question,
        "Answer": answer,
        "InputTokens": input_tokens,
        "OutputTokens": output_tokens
    })

print("Token counting for the sample is complete.")

# 4. Save the detailed sample analysis to a CSV
df_sample = pd.DataFrame(results)
df_sample.to_csv(OUTPUT_FILENAME, index=False)
print(f"Detailed analysis for the {SAMPLE_SIZE}-item sample saved to '{OUTPUT_FILENAME}'")

# 5. Calculate total tokens from our sample and project costs
total_input_tokens = df_sample['InputTokens'].sum()
total_output_tokens = df_sample['OutputTokens'].sum()

print("\n" + "="*60)
print(f"           COST ANALYSIS FOR THE {SAMPLE_SIZE}-ITEM SAMPLE")
print("="*60)
print(f"Total Input Tokens for the sample: {total_input_tokens:,}")
print(f"Total Output Tokens for the sample: {total_output_tokens:,}")
print(f"Average Input Tokens per item in sample: {df_sample['InputTokens'].mean():,.2f}")
print(f"Average Output Tokens per item in sample: {df_sample['OutputTokens'].mean():,.2f}")
print("-" * 60)
print("Projected cost for running ONE framework:")
print("-" * 60)

for model, prices in MODEL_PRICING.items():
    input_cost = (total_input_tokens / 1_000_000) * prices['input']
    output_cost = (total_output_tokens / 1_000_000) * prices['output']
    total_cost = input_cost + output_cost
    
    # The :<15 aligns the text to the left in a 15-character space
    print(f"Model: {model:<15} | Input Cost: ${input_cost:7.4f} | Output Cost: ${output_cost:7.4f} | TOTAL: ${total_cost:7.4f}")

print("-" * 60)
print(f"NOTE: To run both Jac and DSPy, the total cost would be double the amounts listed above.")
print("="*60)