from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employe
from .serializers import EmployeSerializer
from django.shortcuts import get_object_or_404
import qrcode
import base64
from io import BytesIO
import json
import os

@api_view(['GET'])
def list_employes(request):
    employes = Employe.objects.all()
    serializer = EmployeSerializer(employes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_employe(request):
    serializer = EmployeSerializer(data=request.data)
    if serializer.is_valid():
        employe = serializer.save()
        return Response(EmployeSerializer(employe).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    serializer = EmployeSerializer(employe)
    return Response(serializer.data)

@api_view(['PUT'])
def update_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    serializer = EmployeSerializer(employe, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    employe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def generer_qrcode_employe(request, id):
    employe = get_object_or_404(Employe, id=id)

    data = {
        'id': employe.id,
        'nom': employe.nom,
        'prenom': employe.prenom,
        'cin': employe.cin,
        'adresse': employe.adresse,
        'telephone': employe.telephone,
    }

    qr_data = json.dumps(data)
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

    photo_base64 = None
    if employe.photo and os.path.exists(employe.photo.path):
        with open(employe.photo.path, "rb") as image_file:
            photo_base64 = base64.b64encode(image_file.read()).decode()

    return Response({
        'qrcode': qr_image_base64,
        'photo': photo_base64,
        'infos': data
    }, status=status.HTTP_200_OK)
