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
    
    def update(self, instance, validated_data):
        for field in self.Meta.fields:
            if field in validated_data and field not in ['trailers','cast']:
                setattr(instance, field, validated_data[field])
        instance.save()

        if 'trailers' in validated_data:
            for trailer_data in validated_data['trailers']:
                trailer, created = Trailers.objects.update_or_create(movie=instance, url=trailer_data['url'], defaults=trailer_data)
                if not created:
                    trailer.save()

        if 'cast' in validated_data:
            for cast_data in validated_data['cast']:
                cast, created = Cast.objects.update_or_create(movie=instance, character=cast_data['character'], defaults=cast_data)
                if not created:
                    cast.save()

        return instance

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title_korean', 'title_original', 'year', 'poster', 'rating_percent', 'rating_average', 'rating_votes', 'runtime')