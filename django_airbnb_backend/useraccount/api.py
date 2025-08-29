from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import User
from .serializers import UserDetailSerializer
from rest_framework.permissions import IsAuthenticated
from property.serializers import ReservationsListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    serializer = UserDetailSerializer(user, context={'request': request})

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reservations_list(request):
    reservations = request.user.reservations.all()

    print('user', request.user)
    print(reservations)
    
    serializer = ReservationsListSerializer(reservations, many=True)
    return Response(serializer.data)