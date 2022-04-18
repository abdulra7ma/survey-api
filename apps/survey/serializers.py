from account.models import User
from account.serializers import UserSerializer
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import Answer, Question, Surveys


class SurveySerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Surveys
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "description",
            "users",
        ]
        extra_kwargs = {"name": {"error_messages": {"required": True}}}
        read_only_fields = ["id"]

    def create(self, validated_data):
        survey = Surveys.objects.create(**validated_data)
        survey.save()

        if self.initial_data.get("users"):
            # get all the users ids, and remove the duplicate values to decrease
            # the number of database access and code iteration
            user_ids = set([v["id"] for v in self.initial_data.get("users")])

            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)
                    survey.users.add(user)
                except User.DoesNotExist:
                    raise APIException(
                        detail=f"User with id {user_id} does not exists",
                        code=status.HTTP_404_NOT_FOUND,
                    )
        return survey


class RegularUserSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Surveys
        fields = ["id", "name", "start_date", "end_date", "description"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ["id"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "question_type", "survey"]
        read_only_fields = ["id"]


class QuestionAnswerUserSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ["id", "text", "question_type", "answer"]
        read_only_fields = ["id"]

    def get_answer(self, obj):
        answer = Answer.objects.filter(
            Q(question=obj) & Q(user=self.context["user"])
        )
        return AnswerTextSerailizer(instance=answer.first()).data
    
class AnswerTextSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "answer_text"]
        read_only_fields = ["id"]


class SurveyUserAnswerSearializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Surveys
        fields = [
            "id",
            "name",
            "description",
            "user",
            "start_date",
            "end_date",
            "questions",
        ]

    def get_questions(self, obj):
        return QuestionAnswerUserSerializer(
            Question.objects.filter(survey=obj),
            many=True,
            context=self.context,
        ).data

    def get_user(self, obj):
        return UserSerializer(instance=self.context["user"]).data


