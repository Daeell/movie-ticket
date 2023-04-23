from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer, MovieListSerializer
from django.conf import settings

class MovieCollection(APIView):
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title_korean', 'title_original', 'year', 'director']
    filterset_fields = {
        'year' : ['gte', 'lte']
    }
    ordering_fields = ['title_korean', 'year', 'rating_percent', 'runtime']
    
    def get(self, request: Request) -> Response:
        queryset = Movie.objects.all()
        sort = request.query_params.get('sort', None)

        if sort:
            if sort not in self.ordering_fields:
                raise ValueError('유효하지 않은 분류 기준입니다')
            queryset = queryset.order_by(sort)
        
        filtered_queryset = self.filter_queryset(queryset)
        serializer = MovieListSerializer(filtered_queryset, many=True)

        return Response(serializer.data)
        
    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():
            title_korean = serializer.validated_data['title_korean']
            title_original = serializer.validated_data['title_original']
            existing_movie = Movie.objects.filter(title_korean=title_korean, title_original=title_original).first()

            if existing_movie:
                return Response({'error': '영화가 이미 존재합니다.'},status=status.HTTP_409_CONFLICT)

            try:
                movie = serializer.save()
                return Response({'id': movie.id},
                status=status.HTTP_201_CREATED)

            except Exception as e:
                if settings.DEBUG:
                    raise
                else:
                    return Response({'error':'내부 서버 오류가 발생했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetail(APIView):
    def get_object(self, movie_id):
        try:
            return Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise Http404('영화를 찾을 수 없습니다.')
    
    def get(self, request: Request, movie_id) -> Response: 
        movie = self.get_object(movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, movie_id):
        movie = self.get_object(movie_id)
        serializer = MovieSerializer(movie, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error' : '잘못된 요청입니다. 올바른 데이터를 전송해주세요.'}, status=status.HTTP_400_BAD_REQUEST)