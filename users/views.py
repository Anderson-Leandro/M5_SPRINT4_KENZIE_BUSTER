from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
from .permissions import IsOwnerOrAdmin


class UserView(APIView):
    def get(self, request: Request):
        return Response({"msg": "olá get"})

    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request: Request, user_id):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id):
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)
