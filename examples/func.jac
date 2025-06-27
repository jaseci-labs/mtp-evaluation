import from mtllm.llms {OpenAI}

# Initialize the LLM
glob llm = OpenAI(model_name="gpt-4o");

# Define a type-safe LLM function
def calculate_age(cur_year: int, dob: str) -> int by llm();

with entry {
    age = calculate_age(cur_year=2025, dob="1998");
    print(f"Age: {age}");  # Output is guaranteed to be an integer
}