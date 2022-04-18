from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
    openapi.Info(
        title="Survey API",
        default_version="v1",
        description="Test description",
        terms_of_service="",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

token_urlpatterns = [
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/access",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "token/verify",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
]

api_urlpatterns = [
    path("auth/", include("account.urls")),
    path("poll/", include("survey.urls")),
]

main_urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns + token_urlpatterns)),
]

urlpatterns = main_urlpatterns + swagger_urlpatterns
