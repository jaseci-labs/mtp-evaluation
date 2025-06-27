import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj Person {
    has name: str;
    has dob: str;

    # Method uses object state (self) for computation
    def calculate_age(cur_year: int) -> int by llm(incl_info=(self), temperature=0.7);
}

with entry {
    einstein = Person(name="Einstein", dob="March 14, 1879");
    print(f"Einstein's age in 2024: {einstein.calculate_age(2024)}");
}