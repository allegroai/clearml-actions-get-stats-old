"""
Get the statistics of your task's in a project

Need to define in project secrets the follow:
 - TRAINS_API_ACCESS_KEY
 - TRAINS_API_SECRET_KEY
 - TRAINS_API_HOST
"""
import json
import os

from tabulate import tabulate
import pandas as pd
from github3 import login

from trains import Task


def create_output_tables(retrieve_scalars_dict):
    data = []
    for graph_title, graph_values in retrieve_scalars_dict.items():
        graph_data = []
        for series, series_values in graph_values.items():
            graph_data.append((graph_title, series, *series_values.values()))
        data += graph_data
    return sorted(data, key=lambda output: (output[0], output[1]))


def get_task_stats(task_id):
    task = Task.get_task(task_id=task_id)
    if task:
        task_status = task.get_status()
        # Try to get the task stats
        if task_status in ["completed", "published", "publishing", "in_progress", "stopped", "failed"]:
            table = create_comment_output(task, task_status)
            if table:
                return f"Results\n\n{table}\n\n" \
                       f"You can view full task results [here]({task.get_output_log_web_page()})"
            if task_status == "failed":
                return f"No data for task FAILED task {task_id}, " \
                       f"you can view full task results [here]({task.get_output_log_web_page()})"
            else:
                return f"No data yet... You can view full task results [here]({task.get_output_log_web_page()})"
        # Update the user about the task status, can not get any stats
        elif task_status in ["created", "queued", "unknown"]:
            return f"Task is in {task_status} status, no stats yet."
    else:
        return f"Can not find task {task}.\n\n"


def create_comment_output(task, status):
    retrieve_scalars_dict = task.get_last_scalar_metrics()
    if retrieve_scalars_dict:
        scalars_tables = create_output_tables(retrieve_scalars_dict)
        df = pd.DataFrame(data=scalars_tables, columns=["Title", "Series", "Last", "Min", "Max"])
        df.style.set_caption(f"Last scalars metrics for task {task.task_id}, task status {status}")
        table = tabulate(df, tablefmt="github", headers="keys", showindex=False)
        return table


def create_stats_comment(project_stats):
    payload_fname = os.getenv('GITHUB_EVENT_PATH')
    with open(payload_fname, 'r') as f:
        payload = json.load(f)
    owner, repo = payload.get("repository", {}).get("full_name", "").split("/")
    if owner and repo:
        gh = login(token=os.getenv("GITHUB_TOKEN"))
        if gh:
            issue = gh.issue(owner, repo, payload.get("issue", {}).get("number"))
            if issue:
                issue.create_comment(project_stats)
            else:
                print(f'can not comment issue, {payload.get("issue", {}).get("number")}')
        else:
            print(f"can not log in to gh, {os.getenv('GITHUB_TOKEN')}")


if __name__ == "__main__":
    # Get the user input
    base_task_id = os.getenv('INPUT_TASK_ID')
    os.environ["TRAINS_API_ACCESS_KEY"] = os.getenv('INPUT_TRAINS_API_ACCESS_KEY')
    os.environ["TRAINS_API_SECRET_KEY"] = os.getenv('INPUT_TRAINS_API_SECRET_KEY')
    os.environ["TRAINS_API_HOST"] = os.getenv('INPUT_TRAINS_API_HOST')
    stats = get_task_stats(base_task_id)
    create_stats_comment(stats)
