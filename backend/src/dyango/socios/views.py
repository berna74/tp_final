from django.db import DatabaseError, IntegrityError
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Socio
from .serializers import SocioSerializer


def validation_error_payload(serializer):
    return {
        "mensaje": "Datos invalidos",
        "errores": serializer.errors,
    }


class SocioList(generics.ListCreateAPIView):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            data = self.get_serializer(queryset, many=True).data
            return Response(data)
        except DatabaseError:
            return Response([])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            self.perform_create(serializer)
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SocioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Socio.objects.all()
    serializer_class = SocioSerializer

    def _get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            return None

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        socio = self._get_object_or_none()
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(socio).data)

    def update(self, request, *args, **kwargs):
        socio = self._get_object_or_none()
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(socio, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            self.perform_update(serializer)
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        socio = self._get_object_or_none()
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(socio)
        return Response({"mensaje": "Socio eliminado"})
