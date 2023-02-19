from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CustomPermission
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]

    def get(self, request: Request):
        movies = Movie.objects.all()

        pages = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(pages, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, added_by=request.user.email)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]

    def get(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id):
        movie_obj = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, movie=movie_obj)

        return Response(serializer.data, status.HTTP_201_CREATED)
