from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from .auth_jwt import CustomTokenObtainPairView
from .views import (
    CobroDetail,
    CobroList,
    CobroLoteCreate,
    CobroMatrizDosAnios,
    CobroResumenAnual,
    MovimientoFinancieroDetail,
    MovimientoFinancieroList,
    PagoDetail,
    PagoList,
    SocioDetail,
    SocioList,
)


urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r"^socios/?$", SocioList.as_view()),
    re_path(r"^socios/(?P<pk>\d+)/?$", SocioDetail.as_view()),
    re_path(r"^cobros/?$", CobroList.as_view()),
    re_path(r"^cobros/lote/?$", CobroLoteCreate.as_view()),
    re_path(r"^cobros/resumen/?$", CobroResumenAnual.as_view()),
    re_path(r"^cobros/matriz-dos-anios/?$", CobroMatrizDosAnios.as_view()),
    re_path(r"^cobros/(?P<pk>\d+)/?$", CobroDetail.as_view()),
    re_path(r"^pagos/?$", PagoList.as_view()),
    re_path(r"^pagos/(?P<pk>\d+)/?$", PagoDetail.as_view()),
    re_path(r"^movimientos-financieros/?$", MovimientoFinancieroList.as_view()),
    re_path(r"^movimientos-financieros/(?P<pk>\d+)/?$", MovimientoFinancieroDetail.as_view()),
]
