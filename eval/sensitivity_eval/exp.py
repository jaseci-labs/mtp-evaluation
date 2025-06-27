from  datetime import datetime
import os
import subprocess
import pandas as pd

trials = 50

def codeRun(cmd: list[str]):
    subEnv = os.environ.copy()

    start = datetime.now()
    res = subprocess.check_output(cmd, env=subEnv, stderr=subprocess.STDOUT).decode()
    duration = datetime.now() - start
    return res, duration.total_seconds()

def getJacFiles(folder: str) -> list[str]:
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".jac")]

def save(res):
    df = pd.DataFrame(
        res,
        columns=[
            "CodeVariant",
            "Trial",
            "Output",
            "Failed",
            "Time(s)",
            "Exception",
        ],
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date = datetime.now().strftime("%Y-%m-%d")
    df.to_csv(f"sensitivity_eval_{date}_{timestamp}.csv")

res =[]

codeVariants = getJacFiles("code")
for code in codeVariants:
    print(f"Running {code}")
    for trial in range(trials):
        print(f"Trial {trial+1}")
        jacFailed = False
        try:
            jacResponse, jacTimer = codeRun(
                ["jac", "run", code]
            )
            jacResponse = jacResponse.strip()
            exception = ""
        except KeyboardInterrupt:
            exit(1)
        except subprocess.CalledProcessError as e:
            error_output = e.output.decode().splitlines()
            jacFailed = True

        jacResult = [
            code,
            trial,
            jacResponse,
            jacFailed,
            jacTimer,
            exception,
        ]

        res.append(jacResult)
save(res)