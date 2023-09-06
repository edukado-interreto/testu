from django.contrib.auth import get_user_model
from django.core.mail import mail_admins, send_mail
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext as _
from django_extensions.db.models import TimeStampedModel

from apps.core.utils import long_id

User = get_user_model()


CEFR = models.IntegerChoices("CEFR", "A1 A2 B1 B2 C1 C2")


class Tag(TimeStampedModel):
    name = models.CharField("name", max_length=100)

    def __str__(self):
        return self.name


class Exercise(TimeStampedModel):
    CEFR = CEFR

    lid = models.CharField(
        "lid", unique=True, max_length=8, default=long_id, blank=True
    )
    name = models.CharField("name", max_length=100)
    description = models.TextField("description", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    data = models.JSONField("data", default=dict, blank=True)
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
    reactions = models.ManyToManyField(
        User, through="ExerciseReaction", related_name="exercises_liked", blank=True
    )

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


class Exam(TimeStampedModel):
    lid = models.CharField(
        "lid", unique=True, max_length=8, default=long_id, blank=True
    )
    name = models.CharField("name", max_length=100)
    description = models.TextField("description", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.SET_NULL, null=True, blank=True
    )
    accept_submission = models.BooleanField("accept submission", default=False)
    reactions = models.ManyToManyField(
        User, through="ExamReaction", related_name="exams_liked", blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            while self.__class__.objects.filter(lid=self.lid).exists():
                self.lid = long_id()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/exam/{self.lid}"


class Submission(TimeStampedModel):
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    guest = models.CharField("guest", max_length=100, blank=True, null=True)
    exercise = models.ForeignKey(
        Exercise, on_delete=models.SET_NULL, null=True, blank=True
    )
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField("data", default=dict, blank=True)
    score = models.PositiveSmallIntegerField("score", null=True, blank=True)

    def __str__(self):
        fallback = _("NO EXAM OR EXERCISE")
        name = self.exam.name if self.exam else getattr(self.exercise, "name", fallback)
        user = self.created_by.get_username() if self.created_by else self.guest
        return f"{user} for {name}"

    class Meta:
        ordering = ["-created"]


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


class Reaction(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True


class ExerciseReaction(Reaction):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "exercise"],
                name="unique_user_exercise_reaction",
            )
        ]

    def __str__(self):
        return f"{self.user} liked: {self.exercise}"


class ExamReaction(Reaction):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "exam"],
                name="unique_user_exam_reaction",
            )
        ]

    def __str__(self):
        return f"{self.user} liked: {self.exam}"


class Report(TimeStampedModel):
    class ReportType(models.TextChoices):
        MISTAKE = "mistake", _("mistake")
        MISUSE = "misuse", _("misuse")

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="reports"
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.SET_NULL, null=True, related_name="reports"
    )
    nature = models.CharField(
        choices=ReportType.choices, max_length=7, default=ReportType.MISTAKE
    )
    description = models.TextField(default="", blank=True)

    def send_for_mistake(self):
        author = self.exercise.created_by
        text = render_to_string("emails/mistake_body.txt", {"report": self})
        return send_mail(
            subject=f"{ self.user.username } think you made a mistake",
            message=text,
            from_email=None,
            recipient_list=[f"{author.username} <{ author.email }>"],
            fail_silently=False,
        )

    def send_for_misuse(self):
        with translation.override("eo"):
            text = render_to_string("emails/misuse_body.txt", {"report": self})
            return mail_admins(
                subject=f"Misuse: { self.user.username } reported an exercise",
                message=text,
                fail_silently=False,
            )


@receiver(post_save, sender=Report)
def report_by_email(sender, instance, *args, **kwargs):
    getattr(instance, f"send_for_{instance.nature}")()


@receiver(post_delete, sender=UploadedFile)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.file.delete(save=False)
    except:
        pass
