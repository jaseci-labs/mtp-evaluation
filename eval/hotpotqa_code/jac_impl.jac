import os;
import from mtllm.llms {OpenAI}

glob model_name = os.environ["MODEL_NAME"];
glob llm = OpenAI(model_name=model_name);

def get_answer(question: str, context: str) -> str by llm(method="Chain-of-Thoughts");

with entry{
    question = input();
    context = input();
    answer = get_answer(question=question, context=context);
    print(answer);
}