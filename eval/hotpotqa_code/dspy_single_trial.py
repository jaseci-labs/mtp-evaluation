import dspy
import os
model_name = os.environ["MODEL_NAME"]
llm = dspy.LM(model=model_name, max_tokens=1000)
dspy.configure(lm=llm)

class GetAnswer(dspy.Signature):
    """Get the answer to the given question using the given context."""

    question: str = dspy.InputField(desc="The question to be answered.")
    context: str = dspy.InputField(desc="The context to be used for answering the question.")
    answer: str = dspy.OutputField(desc="The answer to the question.")

question = input()
context = input()
response = dspy.Predict(GetAnswer)(question=question, context=context)
print(response.answer)