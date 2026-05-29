import json

from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Socio


PAGE_SIZE = 10


def parse_json(request):
    try:
        return json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return None


def response_item(data, status=200):
    response = JsonResponse(data, status=status, safe=not isinstance(data, list))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def response_paginated(items, page=1, page_size=PAGE_SIZE):
    total_count = len(items)
    total_pages = max((total_count + page_size - 1) // page_size, 1)
    page = max(min(page, total_pages), 1)
    start = (page - 1) * page_size
    end = start + page_size
    return response_item(
        {
            "items": items[start:end],
            "total_pages": total_pages,
            "total_count": total_count,
            "page_size": page_size,
        }
    )


def serialize_socio(socio):
    return {
        "id": socio.id,
        "nombre": socio.nombre,
        "apellido": socio.apellido,
        "dni": socio.dni,
        "email": socio.email,
        "telefono": socio.telefono,
        "fecha_inscripcion": socio.fecha_inscripcion,
        "profesor_id": socio.profesor_id,
        "registra_deuda": socio.registra_deuda,
        "categorias": [],
    }


@csrf_exempt
def socios_collection(request):
    if request.method == "OPTIONS":
        return response_item({}, status=204)

    if request.method == "GET":
        page = int(request.GET.get("page", 1))
        try:
            socios = Socio.objects.all().order_by("id")
            return response_paginated([serialize_socio(socio) for socio in socios], page=page)
        except DatabaseError:
            return response_paginated([], page=page)

    if request.method == "POST":
        data = parse_json(request)
        if data is None:
            return response_item({"mensaje": "JSON invalido"}, status=400)

        socio = Socio.objects.create(
            nombre=data.get("nombre", ""),
            apellido=data.get("apellido", ""),
            dni=data.get("dni", ""),
            email=data.get("email", ""),
            telefono=data.get("telefono", ""),
            fecha_inscripcion=data.get("fecha_inscripcion"),
            profesor_id=data.get("profesor_id"),
            registra_deuda=data.get("registra_deuda", False),
        )
        return response_item(serialize_socio(socio), status=201)

    return response_item({"mensaje": "Metodo no permitido"}, status=405)


@csrf_exempt
def socio_detail(request, pk):
    if request.method == "OPTIONS":
        return response_item({}, status=204)

    try:
        socio = Socio.objects.get(pk=pk)
    except Socio.DoesNotExist:
        return response_item({"mensaje": "Socio no encontrado"}, status=404)

    if request.method == "GET":
        return response_item(serialize_socio(socio))

    if request.method == "PUT":
        data = parse_json(request)
        if data is None:
            return response_item({"mensaje": "JSON invalido"}, status=400)

        socio.nombre = data.get("nombre", socio.nombre)
        socio.apellido = data.get("apellido", socio.apellido)
        socio.dni = data.get("dni", socio.dni)
        socio.email = data.get("email", socio.email)
        socio.telefono = data.get("telefono", socio.telefono)
        socio.fecha_inscripcion = data.get("fecha_inscripcion", socio.fecha_inscripcion)
        socio.profesor_id = data.get("profesor_id", socio.profesor_id)
        socio.registra_deuda = data.get("registra_deuda", socio.registra_deuda)
        socio.save()

        return response_item(serialize_socio(socio))

    if request.method == "DELETE":
        socio.delete()
        return response_item({"mensaje": "Socio eliminado"})

    return response_item({"mensaje": "Metodo no permitido"}, status=405)
