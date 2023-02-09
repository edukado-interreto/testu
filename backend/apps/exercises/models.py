from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.db.models.signals import post_delete
from django.dispatch import receiver
from apps.core.utils import long_id

User = get_user_model()


CEFR = models.IntegerChoices("CEFR", "A1 A2 B1 B2 C1 C2")


class Tag(TimeStampedModel):
    name = models.CharField("name", max_length=100)


class Exercise(TimeStampedModel):
    CEFR = CEFR

    lid = models.CharField("lid", max_length=8, default=long_id, blank=True)
    name = models.CharField("name", max_length=100)
    description = models.TextField("description", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    data = models.JSONField("data", default=list, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    lang_learn = models.BooleanField("about language", default=True)
    src_lang = models.CharField("source language", max_length=10, blank=True)
    lang_learn_lang = models.CharField("target language", max_length=10, blank=True)
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

    class Meta:
        indexes = [
            models.Index(fields=["lid"], name="exercise_lid_idx"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            while self.__class__.objects.filter(lid=self.lid).exists():
                self.lid = long_id()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/exercise/{self.lid}"


class UploadedFile(TimeStampedModel):
    file_name = models.CharField("file_name", max_length=100, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    class FileType(models.TextChoices):
        IMAGE = "image", "image"
        AUDIO = "audio", "audio"

    file_type = models.CharField(
        max_length=5, choices=FileType.choices, default=FileType.IMAGE
    )
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.file_name


@receiver(post_delete, sender=UploadedFile)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.file.delete(save=False)
    except:
        pass
