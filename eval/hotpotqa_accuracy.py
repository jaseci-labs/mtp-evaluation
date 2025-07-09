from datetime import datetime
import os

from datasets import load_dataset
import subprocess
import pandas as pd
import json

models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]
# models = ["gpt-4o-mini"]
timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
filename = f"ModelSweep-hpqa-{timestamp}.csv"

def codeRun(cmd: list[str], inputs: list[str], modelName: str):
    subEnv = os.environ.copy()
    subEnv["MODEL_NAME"] = modelName
    print(modelName)
    with open("/tmp/STDIN.txt", "w") as inputFile:
        inputFile.write("\n".join(inputs))
    with open("/tmp/STDIN.txt", "r") as inputFile:
        start = datetime.now()
        res = subprocess.check_output(cmd, stdin=inputFile, env=subEnv).decode()
        duration = datetime.now() - start
        return res, duration.total_seconds()


def save(res):
    df = pd.DataFrame(
        res,
        columns=[
            "QuestionID",
            "Question",
            "GivenAnswer",
            "Model",
            "Program",
            "Output",
            "ExactMatch",
            "Failed",
            "Time(s)",
        ],
    )
    df.to_csv(filename)



ds = load_dataset("hotpot_qa", "fullwiki")
train = ds["train"]
print(len(train), "train examples loaded")
res = []
count = 0
for i in train:
    if count == 1:
        exit(0)
    question = i["question"]
    answer_str: str = i["answer"]
    print("Question:", question)
    print("Answer:", answer_str)
    answer = answer_str
    # print("Context:", i["context"])
    for model in models:
        print(f"Running Question {count} with model {model}")
        print(f"Running Question {count} with model {model}")
        dspyFailed = False
        jacFailed = False
        try:
            dspyResponse, dspyTimer = codeRun(
                ["python", "dspy_single_trial.py"],
                input=question,
                modelName=model,
            )
            dspyResponse = dspyResponse.strip()
        except KeyboardInterrupt:
            exit(1)
        except:
            dspyFailed = True
            dspyResponse = ""
            dspyTimer = 0
        dspyResult = [
            count,
            question,
            answer,
            model,
            "DSPy",
            dspyResponse,
            (dspyResponse == answer),
            dspyFailed,
            dspyTimer,
        ]
        print("DSPy Result", dspyResult)
        res.append(dspyResult)

        try:
            jacResponse, jacTimer = codeRun(
                ["jac", "run", "jac_impl.jac"],
                input=question,
                modelName=model,
            )
            jacResponse = jacResponse.strip()
        except KeyboardInterrupt:
            exit(1)
        except:
            jacFailed = True
            jacResponse = ""
            jacTimer = 0
        jacResult = [
            count,
            question,
            answer,
            model,
            "Jac",
            jacResponse,
            (jacResponse == answer),
            jacFailed,
            jacTimer,
        ]
        print("Jac Result", jacResult)
        print("Failed?", jacResult[6])
        res.append(jacResult)

    save(res)
    count += 1
