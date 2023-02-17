from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer


class UserView(APIView):
    def get(self, request: Request):
        return Response({"msg": "olá get"})

    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
