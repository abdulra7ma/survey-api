from django.urls import path
from .views import (
    ListCreateSurveyView,
    SurveyView,
    CreateQuestionView,
    RUDQuestionsView,
    ActivePollsView,
    SurveyQuestionsView,
    SurveyUsersView,
    ListCompletedSurveyView,
    CreateAnwserView,
    AnswerView,
    SurveyUserAnswerView
)

urlpatterns = [
    path("active", ActivePollsView.as_view()),
    path("survey", ListCreateSurveyView.as_view()),
    path("survey/<int:s_id>", SurveyView.as_view()),
    path("survey/<int:s_id>/questions", SurveyQuestionsView.as_view()),
    path("survey/<int:s_id>/users", SurveyUsersView.as_view()),
    path("survey/completed", ListCompletedSurveyView.as_view()),
    path("question", CreateQuestionView.as_view()),
    path("question/<int:q_id>", RUDQuestionsView.as_view()),
    path("answer/<int:ans_id>", AnswerView.as_view()),
    path("answer", CreateAnwserView.as_view()),
    path("survey/<int:s_id>/users/<int:u_id>/answers", SurveyUserAnswerView.as_view())
]
