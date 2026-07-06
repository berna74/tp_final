from django.urls import re_path

from .views import AlumnoDetail, AlumnoList

urlpatterns = [
    re_path(r"^alumnos/?$", AlumnoList.as_view()),
    re_path(r"^alumnos/(?P<pk>\d+)/?$", AlumnoDetail.as_view()),
]
