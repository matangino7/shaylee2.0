from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class Login(APIView):
    def post(self, request):
        user = get_object_or_404(User, id=request.data.get('id'))
        password = request.data.get('password')
        if user.password == password:
            return Response({'detail':'User has been authenticated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'User password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)