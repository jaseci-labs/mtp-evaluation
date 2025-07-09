import os;
import from mtllm.llms {OpenAI}

# glob model_name = os.environ["MODEL_NAME"];
glob llm = OpenAI(model_name='gpt-4o-mini', );
# import from mtllm.llms { Gemini }

# glob llm = Gemini(
#     model_name="gemini-2.0-flash"
# );

def get_answer(question: str, context: str) -> str by llm(method="Chain-of-Thoughts");

with entry{
    print("Enter your question:");
    question = input();
    print("Enter the context:");
    context = input();
    answer = get_answer(question=question, context=context);
    print(answer);
}