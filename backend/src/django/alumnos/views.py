from django.core.paginator import EmptyPage, Paginator
from django.db import DatabaseError, IntegrityError
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Alumno
from .serializers import AlumnoSerializer


def validation_error_payload(serializer):
    return {
        "mensaje": "Datos invalidos",
        "errores": serializer.errors,
    }


class AlumnoList(generics.ListCreateAPIView):
    queryset = Alumno.objects.select_related("profesor").all().order_by("apellido", "nombre")
    serializer_class = AlumnoSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            paginator = Paginator(queryset, 10)
            page_number = request.query_params.get("page", 1)

            try:
                page_obj = paginator.page(page_number)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages if paginator.num_pages else 1)

            serializer = self.get_serializer(page_obj.object_list, many=True)
            return Response(
                {
                    "items": serializer.data,
                    "total_pages": paginator.num_pages if paginator.num_pages else 1,
                    "total_count": paginator.count,
                    "page_size": paginator.per_page,
                }
            )
        except DatabaseError:
            return Response({"items": [], "total_pages": 1, "total_count": 0, "page_size": 10})

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


class AlumnoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.select_related("profesor").all()
    serializer_class = AlumnoSerializer

    def _get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            return None

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        alumno = self._get_object_or_none()
        if alumno is None:
            return Response({"mensaje": "Alumno no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(alumno).data)

    def update(self, request, *args, **kwargs):
        alumno = self._get_object_or_none()
        if alumno is None:
            return Response({"mensaje": "Alumno no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(alumno, data=request.data, partial=partial)
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
        alumno = self._get_object_or_none()
        if alumno is None:
            return Response({"mensaje": "Alumno no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(alumno)
        return Response({"mensaje": "Alumno eliminado"})
