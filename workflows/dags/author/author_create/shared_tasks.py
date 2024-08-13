from airflow.decorators import task
from hooks.backoffice.base import BackofficeHook


@task()
def create_decision_on_curation_choice(**context):
    print("wow")
    print(context)
    data = {
        "action": context["params"]["data"]["value"],
        "workflow_id": context["params"]["workflow_id"],
    }

    return BackofficeHook().request(method="POST", data=data, endpoint="api/decisions/")
