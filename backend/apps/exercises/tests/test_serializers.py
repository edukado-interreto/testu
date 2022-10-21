from http import HTTPStatus

import pytest
from apps.exercises.models import Tag
from django.urls import reverse
from freezegun import freeze_time


@freeze_time("2023/01/01")
@pytest.mark.django_db
class TestSheet:
    url = reverse("sheet-list")

    def test_create_empty_sheet(self, logged_client):
        response = logged_client.post(self.url, {"name": "test"})
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 1,
            "name": "test",
            "description": "",
            "created": "2023-01-01T01:00:00+01:00",
            "modified": "2023-01-01T01:00:00+01:00",
            "data": [],
            "lang_learn": False,
            "src_lang": "",
            "lang_learn_lang": "",
            "created_by": logged_client.user.username,
            "age_min": None,
            "age_max": None,
            "lang_learn_cefr_level_min": None,
            "lang_learn_cefr_level_max": None,
            "tags": [],
            "searchable": False,
        }

    def test_create_filled_sheet(self, logged_client):
        response = logged_client.post(
            self.url,
            {
                "name": "test",
                "description": "priskribo",
                "data": '[{"first": {"nested": "data"}}]',
                "lang_learn": False,
                "src_lang": "eo",
                "lang_learn_lang": "en",
                "age_min": 8,
                "age_max": 10,
                "lang_learn_cefr_level_min": 1,
                "lang_learn_cefr_level_max": 2,
                "tags": [],
                "searchable": True,
            },
        )
        assert response.json() == {
            "id": 1,
            "name": "test",
            "description": "priskribo",
            "created": "2023-01-01T01:00:00+01:00",
            "modified": "2023-01-01T01:00:00+01:00",
            "data": [{"first": {"nested": "data"}}],
            "lang_learn": False,
            "src_lang": "eo",
            "lang_learn_lang": "en",
            "created_by": logged_client.user.username,
            "age_min": 8,
            "age_max": 10,
            "lang_learn_cefr_level_min": 1,
            "lang_learn_cefr_level_max": 2,
            "tags": [],
            "searchable": True,
        }
        assert response.status_code == HTTPStatus.CREATED
