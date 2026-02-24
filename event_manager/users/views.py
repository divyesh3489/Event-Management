from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"detail": "Already authenticated. Log out to register a new account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)