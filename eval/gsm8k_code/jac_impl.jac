# import:py from mtllm.llms, OpenAI;

# glob llm = OpenAI(model_name=model_name);

# can get_answer(question: str) -> int by llm(method="Chain-of-Thoughts");

# with entry{
#     question = input();
#     answer = get_answer(question);
#     print(answer);
# }
import os;
import from mtllm.llms {OpenAI}

glob model_name = os.environ["MODEL_NAME"];
glob llm = OpenAI(model_name=model_name);

def get_answer(question: str) -> int by llm(method="Chain-of-Thoughts");

with entry{
    question = input();
    answer = get_answer(question);
    print(answer);
}