from rest_framework import serializers
from .models import Genre, Keyword, Actor, Director, Movie, Comment
from django.contrib.auth import get_user_model

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class KeywordMovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = '__all__'

    movie_keywords = KeywordMovieSerializer(many=True)
    class Meta:
        model = Keyword
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        field = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('movie','user')
        
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    actors = ActorSerializer(many=True)
    directors = DirectorSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'