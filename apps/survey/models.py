from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class Surveys(models.Model):
    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Surveys")
        ordering = ["id"]

    name = models.CharField(
        max_length=256, default=_("New Survey"), verbose_name=_("Survey name")
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    users = models.ManyToManyField(get_user_model(), blank=True)

    def completed_survey_users(self):
        users = []

        for user in self.users.all():
            survey_questions_set = Question.objects.filter(survey=self)
            questions_answers_set = Answer.objects.filter(
                Q(question__in=survey_questions_set) & Q(user=user)
            )
            if survey_questions_set.count() == questions_answers_set.count():
                if not survey_questions_set.count() == 0:
                    users.append(user)
        return users

    @property
    def is_completed(self):
        return True if len(self.completed_survey_users()) != 0 else False

    def __str__(self):
        return str(self.id) + ": " + self.name


class Question(models.Model):
    class Meta:
        verbose_name = _("Question2")
        verbose_name_plural = _("Questions")
        ordering = ["id"]

    TYPE = (
        (0, _("Single Choice Answer")),
        (1, _("Text Answer")),
        (2, _("Multiple Choice")),
    )

    survey = models.ForeignKey(
        Surveys, on_delete=models.DO_NOTHING, related_name="question"
    )
    text = models.CharField(max_length=255, verbose_name=_("Title"))
    question_type = models.IntegerField(
        choices=TYPE, default=0, verbose_name=_("Type of Question")
    )


class Answer(models.Model):
    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ["id"]

    survey = models.ForeignKey(
        Surveys, related_name="survey", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, related_name="answer", on_delete=models.CASCADE
    )
    answer_text = models.CharField(
        max_length=255, verbose_name=_("Answer Text")
    )
    user = models.ForeignKey(
        get_user_model(), related_name="user", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.answer_text
