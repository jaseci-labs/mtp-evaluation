import from os {environ}
import from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name='gpt-4o');

def get_answer(question: str) -> int by llm(method="Chain-of-Thoughts");

with entry{
    question = "Tobias is buying a new pair of shoes that costs $95. He has been saving up his money each month for the past three months. He gets a $5 allowance a month. He also mows lawns and shovels driveways. He charges $15 to mow a lawn and $7 to shovel. After buying the shoes, he has $15 in change. If he mows 4 lawns, how many driveways did he shovel?";
    answer = get_answer(question);
    print(answer);
}