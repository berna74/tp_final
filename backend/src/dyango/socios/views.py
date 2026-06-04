from django.db import DatabaseError, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Socio
from .serializers import (
    SocioSerializer,
    SociosListQuerySerializer,
    SociosPaginatedResponseSerializer,
)


PAGE_SIZE = 10


def paginated_payload(items, page=1, page_size=PAGE_SIZE):
    total_count = len(items)
    total_pages = max((total_count + page_size - 1) // page_size, 1)
    page = max(min(page, total_pages), 1)
    start = (page - 1) * page_size
    end = start + page_size
    payload = {
        "items": items[start:end],
        "total_pages": total_pages,
        "total_count": total_count,
        "page_size": page_size,
    }
    serializer = SociosPaginatedResponseSerializer(instance=payload)
    return serializer.data


def validation_error_payload(serializer):
    return {
        "mensaje": "Datos invalidos",
        "errores": serializer.errors,
    }


class CorsAPIView(APIView):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response


class SociosCollectionAPIView(CorsAPIView):
    def get(self, request):
        query_serializer = SociosListQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(
                validation_error_payload(query_serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )
        page = query_serializer.validated_data["page"]

        try:
            socios = Socio.objects.all().order_by("id")
            data = SocioSerializer(socios, many=True).data
            return Response(paginated_payload(data, page=page))
        except DatabaseError:
            return Response(paginated_payload([], page=page))

    def post(self, request):
        serializer = SocioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            socio = serializer.save()
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(SocioSerializer(socio).data, status=status.HTTP_201_CREATED)


class SocioDetailAPIView(CorsAPIView):
    def get_object(self, pk):
        try:
            return Socio.objects.get(pk=pk)
        except Socio.DoesNotExist:
            return None

    def get(self, request, pk):
        socio = self.get_object(pk)
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(SocioSerializer(socio).data)

    def put(self, request, pk):
        socio = self.get_object(pk)
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SocioSerializer(socio, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                validation_error_payload(serializer),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            socio = serializer.save()
        except IntegrityError as exc:
            return Response({"mensaje": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(SocioSerializer(socio).data)

    def delete(self, request, pk):
        socio = self.get_object(pk)
        if socio is None:
            return Response({"mensaje": "Socio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        socio.delete()
        return Response({"mensaje": "Socio eliminado"})
