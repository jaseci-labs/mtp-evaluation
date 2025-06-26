import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

def get_reason_and_oddword(options: list[str]) -> tuple[str, str] by llm();

with entry {
    print(get_reason_and_oddword(["Bentley", "Ferrari", "Lamborghini", "Casio", "Toyota"]));
}
