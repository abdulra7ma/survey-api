from django.contrib import admin
from .models import Surveys, Question, Answer

admin.site.register(Surveys)
admin.site.register(Question)
admin.site.register(Answer)
