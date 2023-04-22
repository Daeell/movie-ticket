from rest_framework import serializers
from .models import Movie, Trailers, Cast

class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailers
        fields = ('url', 'type')

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ('actor', 'character')

class MovieSerializer(serializers.ModelSerializer):
    trailers = TrailerSerializer(many=True)
    cast = CastSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('id', 'title_korean', 'title_original', 'year', 'poster', 'rating_percent', 'rating_average', 'rating_votes', 'runtime', 'director', 'trailers', 'cast', 'synopsis')
    
    def create(self, validated_data):
        trailers_data = validated_data.pop('trailers')
        cast_data = validated_data.pop('cast')

        movie = Movie.objects.create(**validated_data)

        for trailer_data in trailers_data:
            Trailers.objects.create(movie=movie, **trailer_data)
        
        for cast_item in cast_data:
            Cast.objects.create(movie=movie, **cast_item)
        
        return movie

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title_korean', 'title_original', 'year', 'poster', 'rating_percent', 'rating_average', 'rating_votes', 'runtime')