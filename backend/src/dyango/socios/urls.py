from django.urls import re_path

from .views import SocioDetailAPIView, SociosCollectionAPIView


urlpatterns = [
    re_path(r"^socios/?$", SociosCollectionAPIView.as_view()),
    re_path(r"^socios/(?P<pk>\d+)/?$", SocioDetailAPIView.as_view()),
]
