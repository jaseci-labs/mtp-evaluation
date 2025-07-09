import pandas as pd
from datasets import load_dataset
import tiktoken
import matplotlib.pyplot as plt
import numpy as np

print("Starting analysis of HotpotQA token counts...")

# 1. Load the dataset
ds = load_dataset("hotpot_qa", "fullwiki")
train_data = ds["train"]
print(f"Loaded {len(train_data)} examples from the train set.")

# 2. Initialize the tokenizer for OpenAI models
# "cl100k_base" is the encoding used by gpt-4, gpt-3.5-turbo, and gpt-4o models
try:
    encoding = tiktoken.get_encoding("cl100k_base")
except Exception:
    encoding = tiktoken.encoding_for_model("gpt-4")

# 3. Process the dataset to count tokens
results = []
token_counts = []

print("Iterating through dataset to count tokens... (This may take a few minutes)")
for idx, item in enumerate(train_data):
    # The full context is the combination of titles and sentences
    context_titles = " ".join(item['context']['title'])
    # The sentences are a list of lists, so we flatten them first
    context_sentences = " ".join(sum(item['context']['sentences'], []))
    full_context = context_titles + " " + context_sentences
    question = item['question']
    
    # We simulate the full prompt that would be sent to the model
    # A common format is to combine context and question
    input_prompt = f"Context: {full_context}\n\nQuestion: {question}"
    
    # Count the tokens
    num_tokens = len(encoding.encode(input_prompt))
    
    token_counts.append(num_tokens)
    results.append({
        "QuestionID": item['id'],
        "Question": question,
        "ContextTokenCount": num_tokens
    })
    if (idx + 1) % 10000 == 0:
        print(f"Processed {idx + 1}/{len(train_data)} examples...")

print("Token counting complete.")

# 4. Save the detailed token counts to a CSV
df = pd.DataFrame(results)
output_csv_filename = "hotpotqa_token_analysis.csv"
df.to_csv(output_csv_filename, index=False)
print(f"Token analysis saved to {output_csv_filename}")

# 5. Generate and save the histogram plot
plt.figure(figsize=(12, 6))
plt.hist(token_counts, bins=100, color='skyblue', edgecolor='black')
plt.title('Distribution of Input Token Counts in HotpotQA (Context + Question)')
plt.xlabel('Number of Tokens')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)

# Add lines for mean and median
mean_val = np.mean(token_counts)
median_val = np.median(token_counts)
plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_val:.0f}')
plt.axvline(median_val, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median_val:.0f}')
plt.legend()

plot_filename = "hotpotqa_token_distribution.png"
plt.savefig(plot_filename)
print(f"Distribution plot saved to {plot_filename}")

# 6. Print summary statistics 
print("\n--- Summary Statistics for Input Tokens ---")
print(f"Minimum Tokens: {np.min(token_counts)}")
print(f"Maximum Tokens: {np.max(token_counts)}")
print(f"Average (Mean) Tokens: {mean_val:.2f}")
print(f"Median Tokens: {median_val:.2f}")
print("-----------------------------------------")
print(f"\nAnalysis complete. Based on this, you can decide on a sample size for your main evaluation.")