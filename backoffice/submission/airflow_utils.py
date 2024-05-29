import re

import requests
from django.http import JsonResponse
from requests.exceptions import HTTPError, RequestException

# TODO specify this variable as an environment variable in the correct place
AIRFLOW_BASE_API_URL = 'http://airflow-webserver:8080/api/v1/'

AIRFLOW_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Basic YWlyZmxvdzphaXJmbG93"
}

AUTHOR_DAG_IDS=["author_create_initialization_dag","author_create_approved_dag","author_create_rejected_dag"]

def trigger_airflow_dag(dag_id,workflow_id, extra_data = None):
    """ triggers an airflow dag
    :param dag_id: name of the dag to run
    :param workflow_id: id of the workflow being triggered
    :return request response"""

    # set dag_run_id to be the workflow_id for simplicity, as each workflow should only run once
    # upon failure it can be rerun keeping the same id
    # TODO check and remove if conf: workflow_id can be removed
    data = {
        "dag_run_id": workflow_id,
        "conf":
            {
                "workflow_id": workflow_id
            }
        }
    
    if extra_data is not None:
        data["conf"].update(extra_data)

    url = f'{AIRFLOW_BASE_API_URL}/dags/{dag_id}/dagRuns'

    try:
        response = requests.post(url, json=data, headers=AIRFLOW_HEADERS, timeout=300)
        response.raise_for_status()
        return JsonResponse(response.json())
    except HTTPError as http_err:
        return JsonResponse({'error': f'HTTP error occurred: {http_err}'}, status=response.status_code)
    except RequestException as req_err:
        return JsonResponse({'error': f'Request error occurred: {req_err}'}, status=500)

# Helper function to fetch DAG runs
def get_dag_runs(dag_id):
    response = requests.get(f'{AIRFLOW_BASE_API_URL}/dags/{dag_id}/dagRuns', headers=AIRFLOW_HEADERS)
    response.raise_for_status()
    return response.json()['dag_runs']

# Helper function to fetch task instances for a DAG run
def get_task_instances(dag_id, dag_run_id):
    response = requests.get(f'{AIRFLOW_BASE_API_URL}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances', headers=AIRFLOW_HEADERS)
    response.raise_for_status()
    return response.json()['task_instances']

# Helper function to fetch logs for a specific task instance
def get_task_logs(dag_id, dag_run_id, task_id, try_number):
    response = requests.get(f'{AIRFLOW_BASE_API_URL}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{try_number}', headers=AIRFLOW_HEADERS)
    response.raise_for_status()
    return response.text

# Helper function to extract the traceback from logs
def extract_traceback(log):
    pattern = r'Traceback \(most recent call last\):\s+(?:  File "(.*?)", line (\d+), in (\w+)\s+([^\n]+)\n)+([^\n]+Error: (.+?))\n'

    traceback_pattern = re.compile(pattern, re.MULTILINE)
    match = traceback_pattern.search(log)
    return match.group(0) if match else None