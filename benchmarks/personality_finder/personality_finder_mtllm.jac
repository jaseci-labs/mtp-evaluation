import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o");

enum Personality {
   INTROVERT = "Introvert",
   EXTROVERT = "Extrovert"
}

obj Person {
    has full_name: str,
        yod: int,
        personality: Personality;
}

def get_person_info(name: str) -> Person by llm();

with entry {
    person_obj = get_person_info('Martin Luther King Jr.');
    print(f"{person_obj.full_name} was a {person_obj.personality.value} person who died in {person_obj.yod}");
}