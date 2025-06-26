import dspy


llm = dspy.LM('openai/gpt-4o')

dspy.configure(lm=llm)

question = input()
answer = dspy.TypedChainOfThought('question:str -> answer:int', max_retries=1)
response = answer(question=question)

print(response.answer)