import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

obj Person {
    has name: str;
    has dob: str;
}

with entry {
    # LLM fills in missing field based on partial information
    einstein = Person(name="Einstein" by llm());
    print(f"{einstein.name} was born on {einstein.dob}");
}