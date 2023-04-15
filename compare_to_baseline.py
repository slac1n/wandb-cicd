import os

import wandb.apis.reports as wr
from ghapi.core import GhApi

import wandb

# check if WANDB_API_KEY is set
assert "WANDB_API_KEY" in os.environ, "WANDB_API_KEY not set"

# check if RUN_ID_TO_COMPARE is set
assert "RUN_ID_TO_COMPARE" in os.environ, "RUN_ID_TO_COMPARE not set"

ENTITY = "frisur_hertz0s"
PROJECT = "cicd-quickstart"

# get run with baseline tag using MONGO API
api = wandb.Api()
tags = ["baseline"]

# get all runs with baseline tag using MONGO API
baseline_runs = api.runs(f"{ENTITY}/{PROJECT}", {"tags": {"$in": tags}})

# get all run names
baseline_names = [run.name for run in baseline_runs]
# get first run name
baseline_name = baseline_names[0]


# get run with run id
run = api.run(f"{ENTITY}/{PROJECT}/{os.environ['RUN_ID_TO_COMPARE']}")

# get run name
run_name = run.name


# create report
report = wr.Report(
    PROJECT,
    ENTITY,
    title="Compare to baseline",
    description=f"Run is compared to baseline which is {baseline_name}",
)

pg = wr.PanelGrid(
    runsets=[
        wr.Runset(ENTITY, PROJECT, "RUN Comparision").set_filters_with_python_expr(
            f"Name in ['{baseline_name}', '{run_name}']"
        )
    ],
    panels=[
        wr.RunComparer(diff_only="split", layout={"width": 100, "height": 200}),
    ],
)
report.blocks = report.blocks[:1] + [pg] + report.blocks[1:]
report.save()

number = os.environ["ISSUE_NUMBER"]
owner, repo = os.environ["REPO"].split("/")
print(number, owner, repo)
gitapi = GhApi(owner=owner, repo=repo)
gitapi.issues.create_comment(
    number,
    f"Hi, this is the link for the baseline comparision report you requested:",
)
