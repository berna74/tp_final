from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from .auth_jwt import CustomTokenObtainPairView
from .views import SocioList, SocioDetail


urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r"^socios/?$", SocioList.as_view()),
    re_path(r"^socios/(?P<pk>\d+)/?$", SocioDetail.as_view()),
]
