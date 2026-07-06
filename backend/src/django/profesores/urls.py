from django.urls import re_path

from .views import ProfesorDetail, ProfesorList

urlpatterns = [
    re_path(r"^profesores/?$", ProfesorList.as_view()),
    re_path(r"^profesores/(?P<pk>\d+)/?$", ProfesorDetail.as_view()),
]
