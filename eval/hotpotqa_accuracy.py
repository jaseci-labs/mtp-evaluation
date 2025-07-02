from datetime import datetime
import os

from datasets import load_dataset
import subprocess
import pandas as pd
import json

models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]
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
res = []
count = 0
for i in train:
    if count == 10:
        exit(0)
    print("Question:", i["question"])
    print("Answer:", i["answer"])
    print("Context:", i["context"])
    # question = i["question"][0]
    # answer_str: str = i["answer"][0]
    # answer = answer_str.split(" ")[-1].replace(",", "")
    # for model in models:
    #     print(f"Running Question {count} with model {model}")
    #     dspyFailed = False
    #     jacFailed = False
    #     try:
    #         dspyResponse, dspyTimer = codeRun(
    #             ["python", "gsm8k_code/dspy_single_trial.py"],
    #             input=question,
    #             modelName=model,
    #         )
    #         dspyResponse = dspyResponse.strip()
    #     except KeyboardInterrupt:
    #         exit(1)
    #     except:
    #         dspyFailed = True
    #         dspyResponse = ""
    #         dspyTimer = 0
    #     dspyResult = [
    #         count,
    #         question,
    #         answer,
    #         model,
    #         "DSPy",
    #         dspyResponse,
    #         (dspyResponse == answer),
    #         dspyFailed,
    #         dspyTimer,
    #     ]
    #     print("DSPy Result", dspyResult)
    #     res.append(dspyResult)

    #     try:
    #         jacResponse, jacTimer = codeRun(
    #             ["jac", "run", "gsm8k_code/jac_impl.jac"],
    #             input=question,
    #             modelName=model,
    #         )
    #         jacResponse = jacResponse.strip()
    #     except KeyboardInterrupt:
    #         exit(1)
    #     except:
    #         jacFailed = True
    #         jacResponse = ""
    #         jacTimer = 0
    #     jacResult = [
    #         count,
    #         question,
    #         answer,
    #         model,
    #         "Jac",
    #         jacResponse,
    #         (jacResponse == answer),
    #         jacFailed,
    #         jacTimer,
    #     ]
    #     print("Jac Result", jacResult)
    #     res.append(jacResult)

    # save(res)
    count += 1
