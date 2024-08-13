import pytest
from dags.author.author_create.shared_tasks import (
    create_decision_on_curation_choice,
)


class TestAuthorCreate:
    context = {
        "params": {
            "workflow_id": "ecaa62db-1326-43cf-8885-da96c544af42",
            "data": {
                "value": "create",
            },
        }
    }

    @pytest.mark.vcr()
    def test_create_decision_on_curation_choice(self):
        result = create_decision_on_curation_choice.function(**self.context)
        assert result.status_code == 201
