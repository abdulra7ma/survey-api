import datetime

from account.models import User
from account.serializers import UserSerializer
from lib.utils.helpers import get_query_id
from rest_framework import generics, mixins, status, views
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Answer, Question, Surveys
from django.db.models import Count
from .permissions import IsAdministrator
from .serializers import (
    AnswerSerializer,
    QuestionSerializer,
    RegularUserSurveySerializer,
    SurveySerializer,
    SurveyUserAnswerSearializer,
)
from lib.utils.helpers import get_model_object
from django.db.models import DateTimeField, ExpressionWrapper, F, BooleanField


class ActivePollsView(generics.ListAPIView):
    """
    Get all the active polls
    """

    serializer_class = SurveySerializer

    def get_queryset(self):
        return Surveys.objects.filter(end_date__gte=datetime.date.today())

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if hasattr(self.request.user, "is_administrator"):
            if not self.request.user.is_administrator:
                return RegularUserSurveySerializer
            return SurveySerializer
        return RegularUserSurveySerializer


class ListCreateSurveyView(generics.ListCreateAPIView):
    """
    Get Surveys instance and related questions.
    Return all the surveys object related to logged in user,
    if the user is administarator it return all the surveys object that if avalibale
    """

    serializer_class = SurveySerializer
    authentication_classes = []

    def get_queryset(self):
        print(self.request.user.is_administrator)
        return (
            Surveys.objects.filter(users__id=self.request.user.id)
            if not self.request.user.is_administrator
            else Surveys.objects.all()
        )

    def list(self, request, *args, **kwargs):
        return Response(
            data=self.get_serializer(self.get_queryset(), many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        """
        Create a survey object
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if hasattr(self.request.user, "is_administrator"):
            if not self.request.user.is_administrator:
                return RegularUserSurveySerializer
            return SurveySerializer
        return RegularUserSurveySerializer


class SurveyView(views.APIView):
    """
    Update, Retrieve and Delete Survey instance.
    **NOTE: For updating the survey instace PATCH is used
    """

    serializer_class = SurveySerializer
    permission_classes = [IsAdministrator]

    def get_object(self):
        try:
            return Surveys.objects.get(id=self.kwargs["s_id"])
        except Surveys.DoesNotExist:
            raise APIException("Survey with given id not found")

    def get(self, request, *args, **kwargs):
        """
        Get survey object by ID
        """
        return Response(
            data=self.serializer_class(instance=self.get_object()).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        """
        Updated survey object by ID
        """
        serializer = self.serializer_class(
            instance=self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Delete survey object by ID
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class CreateQuestionView(generics.CreateAPIView):
    """
    Create a new question instance
    """

    serializer_class = QuestionSerializer
    permission_classes = [IsAdministrator]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RUDQuestionsView(views.APIView):
    """
    Retrieve, Update and Delete Question instance.
    **NOTE: For updating the Question instace PATCH is used
    """

    serializer_class = QuestionSerializer
    permission_classes = [IsAdministrator]

    def get_object(self):
        try:
            return Question.objects.get(id=self.kwargs["q_id"])
        except Question.DoesNotExist:
            raise APIException("Question with given id not found")

    def get(self, request, *args, **kwargs):
        """
        Get question object by ID
        """
        return Response(
            data=self.serializer_class(instance=self.get_object()).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        """
        Update question object by ID
        """
        serializer = self.serializer_class(
            instance=self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Delete question object by ID
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class SurveyQuestionsView(generics.ListAPIView):
    """
    API view that returns all the questions related to one survey
    """

    serializer_class = QuestionSerializer
    # permission_classes = [IsAdministrator]

    def get_queryset(self):
        survey = Surveys.objects.filter(id=self.kwargs["s_id"])

        if survey.exists():
            return Question.objects.filter(survey=survey.first())

        raise APIException("Survey not found.")

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SurveyUsersView(
    mixins.DestroyModelMixin, mixins.CreateModelMixin, generics.ListAPIView
):
    """
    API view that returns all the users related to one survey,
    add/remove user to/from survey.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAdministrator]

    def get_object(self):
        survey = Surveys.objects.filter(id=self.kwargs["s_id"])

        if survey.exists():
            return survey.first()

        raise APIException("Survey not found.")

    def get_queryset(self):
        return self.get_object().users.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        add a new user to the survey users
        """

        for user_id in request.data:
            self.get_object().users.add(get_model_object(User, user_id["id"]))

        return Response(
            data=SurveySerializer(instance=self.get_object()).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        """
        remove a user from the survey users
        """

        for user_id in request.data:
            self.get_object().users.remove(
                get_model_object(User, user_id["id"])
            )

        return Response(
            data=SurveySerializer(instance=self.get_object()).data,
            status=status.HTTP_200_OK,
        )


class ListCompletedSurveyView(generics.ListAPIView):
    """
    Return all the completed surveys and thier users.
    A completed survey is the survey where at least one user
    has answered all the include in that survey.
    """

    serializer_class = SurveySerializer

    def get_queryset(self):
        return [s for s in Surveys.objects.all() if s.is_completed]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AnswerView(views.APIView):
    """
    Update, Retrieve and Delete Survey instance.
    **NOTE: For updating the answer instace PATCH is used
    """

    serializer_class = AnswerSerializer
    permission_classes = []

    def get_object(self):
        try:
            return Answer.objects.get(id=self.kwargs["ans_id"])
        except Answer.DoesNotExist:
            raise APIException("Answer with given id not found")

    def check_object_permissions(self, request, obj):
        """
        Check the object permission if the comming request is GET request
        and give permission to get the object if the request user is the owner
        of the anwer object or the user is administrator
        """
        if request.method == "GET":
            if request.user == obj.user or request.user.is_administrator:
                return True
            else:
                return False
        return True

    def get(self, request, *args, **kwargs):
        """
        Get anwser object by ID
        """
        return Response(
            data=self.serializer_class(instance=self.get_object()).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        """
        Udate anwser object by ID
        """
        serializer = self.serializer_class(
            instance=self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Delete anwser object by ID
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class CreateAnwserView(generics.CreateAPIView):
    """
    Creates new answer instance
    """

    serializer_class = AnswerSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SurveyUserAnswerView(generics.RetrieveAPIView):
    serializer_class = SurveyUserAnswerSearializer

    def get(self, request, *args, **kwargs):
        """
        Get the survey answers related to one user by the specifing the
        survey id and user id
        """
        survey = get_model_object(Surveys, self.kwargs.get("s_id"))
        serializer = self.serializer_class(
            instance=survey, context=self.get_serializer_context()
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        if getattr(self, "swagger_fake_view", False):
            return super().get_serializer_context()

        context = super().get_serializer_context()
        context["user"] = get_model_object(User, self.kwargs.get("u_id"))
        return context
