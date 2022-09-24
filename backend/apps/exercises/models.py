from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class CEFR(models.IntegerChoices):
    A1 = 0
    A2 = 1
    B1 = 2
    B2 = 3
    C1 = 4
    C2 = 5


class Tag(TimeStampedModel):
    name = models.CharField("name", max_length=100)


class Sheet(TimeStampedModel):
    CEFR = CEFR

    name = models.CharField("name", max_length=100)
    description = models.TextField("description", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    data = models.JSONField("data", default=list, blank=True)
    src_lang = models.CharField("source language", max_length=10, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    lang_learn = models.BooleanField("about language", default=True)
    lang_learn_cefr_level_min = models.PositiveSmallIntegerField(
        "CEFR min",
        choices=CEFR.choices,
        null=True,
        blank=True,
    )
    lang_learn_cefr_level_max = models.PositiveSmallIntegerField(
        "CEFR max",
        choices=CEFR.choices,
        null=True,
        blank=True,
    )
    age_min = models.PositiveSmallIntegerField("minimum age", null=True, blank=True)
    age_max = models.PositiveSmallIntegerField("maximum age", null=True, blank=True)
    searchable = models.BooleanField("searchable", default=True)

    def __str__(self):
        return self.name
