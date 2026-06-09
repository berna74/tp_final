from django.urls import re_path

from .views import SocioList, SocioDetail


urlpatterns = [
    re_path(r"^socios/?$", SocioList.as_view()),
    re_path(r"^socios/(?P<pk>\d+)/?$", SocioDetail.as_view()),
]
