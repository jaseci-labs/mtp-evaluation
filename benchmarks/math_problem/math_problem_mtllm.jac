import from os {environ}
import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name='gpt-4o');

def get_answer(question: str) -> int by llm(method="Chain-of-Thoughts");

with entry{
    question = input("Ask your math question: ");
    answer = get_answer(question);
    print(answer);
}