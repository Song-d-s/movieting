from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MovieSerializer, KeywordSerializer, CommentSerializer
from .models import Movie, Keyword, Comment
from django.shortcuts import redirect
import csv
import pandas as pd
import datetime
import json
import os
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@api_view(['POST'])
def surveyPickDone(request):
    user = request.user

    for i in request.data['surveySelectMovies']:
        movie = get_object_or_404(Movie, pk=i)
        
        datas = {
          'content': 'survey',
          'rating': 5,
          'is_survey' : 1,
        }

        serializer = CommentSerializer(data=datas)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)  
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_201_CREATED)

# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    # if request.method == 'GET':
    #     movies = Movie.objects.all()
    #     random_movies = choices(movies, k=10)
    #     # print(movies[0])
    #     # serializer = MovieSerializer(movies, many=True)
    #     serializer = MovieSerializer(random_movies, many=True)
    #     return Response(serializer.data)
    pass

@api_view(['GET', 'POST'])
def detail(request, movie_id):
    if request.method == 'GET':
        movie = Movie.objects.get(id=movie_id)
        serializer = MovieSerializer(movie)

        User = get_user_model()

        for i in range(len(serializer.data['comments'])):
            user = User.objects.filter(id=serializer.data['comments'][i]['user']).values()
            serializer.data['comments'][i]['username'] = user[0]['username']
            serializer.data['comments'][i]['imgUrl'] = user[0]['imgUrl']

        # serializer.data['like_user_len'] = len(serializer.data['like_users'])
        return Response(serializer.data)

@api_view(['GET'])
def popular(request):
    movie = Movie.objects.all().order_by('-popularity')[:10]
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def random(request):
    '''
    ?????? ?????? ????????? filter ??????
    '''
    a = Movie.objects.filter(pk__in=[436270, 882598])
    b = Movie.objects.all().order_by('?')[:20]
    movie = a|b
    movie = movie.distinct()[:20]
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def keyword(request, keyword_id):
    keyword = Keyword.objects.get(id=keyword_id)
    serializer = KeywordSerializer(keyword)
    return Response(serializer.data)

# ?????????
@api_view(['POST'])
def likes(request, movie_id):
    print('????????? django ??????')
    # ???????????? ????????? ?????????~
    if request.user.is_authenticated:
        print('?????? ?????????')
        print('user.is_authenticated')
        movie = Movie.objects.get(pk=movie_id)

        # ????????? ???????????? ???????????? ?????? ???????????? if ?????? ?????????????
        # 2. ?????? ???????????? ???????????? ?????? ?????? ????????? ?????? ???????????? ???????????? ????????? ???????????? ??????.
        # if request.user in article.like_users.all():
        # 1. ?????? ???????????? ???????????? ?????? ???????????? ?????? ???????????? ???????????? ????????? ???????????? ?????????????????? ??????.
        if movie.like_users.filter(pk=request.user.pk).exists():
        # filter??? ?????? get??? ?????? ?????? ??????: get??? ????????? ????????? ???????????? ????????? ????????? ?????????.
            # ????????? ?????? (remove)
            movie.like_users.remove(request.user)
        else:
            # ????????? ?????? (add)
            movie.like_users.add(request.user)
    movies = list(Movie.objects.filter(pk=movie_id).values())
    return Response(movies)

@api_view(['DELETE', 'PUT'])
def comment_edit(request, comment_id):
    print('@@@@@@@@@@@@@????????????', comment_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    print(comment)
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # API??? ????????? ????????? ?????? ????????? ?????????????????? ??????.
    elif request.method == 'PUT':
        print('????????????')
        serializer = CommentSerializer(comment, data=request.data)  # POST??? article ??????????????? ????????? ??????.
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            print('serializer ??????????????? ')
            serializer.save()
            return Response(serializer.data)

@api_view(['POST'])
def comment_create(request, movie_id):
    print('###?????????')
    # movie = Movie.objects.get(pk=movie_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    # user = get_object_or_404(get_user_model(), pk=request.data['user_id'])
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=user)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def test(request):
    print('???!!!!!!!!!!!!!!')
    comment = Comment.objects.filter(user_id=request.user.id).filter(rating=5).order_by('-created_at')

    movie_id_lst = []
    for x in comment:
        movie_id_lst.append(x.movie_id)

    movie_id_lst = list(set(movie_id_lst))
    movies = Movie.objects.filter(id__in=movie_id_lst)
    
    dt_now = datetime.datetime.now()
    user_row = [1050000, '1050000', '1050000', str(dt_now.date()), 1050000, 1050000, '1050000', '1050000', '1050000']
    genres = []
    keywords = []
    
    for x in movies:
        for y in x.genres.all().values():
            genres.append(y['id'])
        for p in x.keywords.all().values():
            keywords.append(p['id'])

    genres = list(set(genres))
    keywords = list(set(keywords))
    user_row.append(genres)
    user_row.append(keywords)
    user_row = user_row + [[],[],1050000,'1050000']
    
    # csv ??? ?????? ??? user ??? ????????? ????????? ??? ???????????? csv??? ??? ?????? ???????????? ??????.
    # ????????? ????????? ?????? ????????? 5?????? ??? 10?????? ????????? ????????????
    # csv ??? ??? ?????? ??????
    # ????????? ??? ???????????? 0 ?????? ?????? ????????? ????????? target_index ??????
    movies_json_to_csv(user_row)
    # target_id = request.data.id
    # print(target_id)
    print('????????????????????????????????')
    result = movies_similarity_genre_set()

    movie = Movie.objects.filter(id__in=result)
    serializer = MovieSerializer(movie, many=True)

    return Response(serializer.data)

def movies_similarity_genre_set(top=30):
    csv_url = os.getcwd() + "\movies\\fixtures\movies.csv"
    df = pd.read_csv(csv_url, encoding='utf-8')

    target_movie_index = 0

    counter_vector = CountVectorizer(ngram_range=(1,3))
    # c_vector_genres = counter_vector.fit_transform(df['genres']+df['keywords'])
    c_vector_genres = counter_vector.fit_transform(df['genres'])
    c_vector_keywords = counter_vector.fit_transform(df['keywords'])

    similarity_genre = cosine_similarity(c_vector_genres, c_vector_genres).argsort()[:, ::-1]
    similarity_keyword = cosine_similarity(c_vector_keywords, c_vector_keywords).argsort()[:, ::-1]

    sim_index = similarity_genre[target_movie_index, :top].reshape(-1)
    sim_index2 = similarity_keyword[target_movie_index, :top].reshape(-1)

    sim_index = sim_index.tolist()
    sim_index2 = sim_index2.tolist()

    # if target_movie_index in sim_index:
    sim_index.remove(0)
    sim_index2.remove(0)

    # if target_movie_index in sim_index2:
    #     sim_index2.remove(target_movie_index)

    # result = df.iloc[sim_index].sort_values('score', ascending=False)[:10]
    result = df.iloc[sim_index].sort_values('vote_average', ascending=False)[:10]['id'].tolist()
    result2 = df.iloc[sim_index2].sort_values('vote_average', ascending=False)[:10]['id'].tolist()
    return result + result2


def movies_json_to_csv(user_row):
    json_url = os.getcwd() + "\movies\\fixtures\movies.json"
    
    with open(json_url, 'r', encoding="utf-8-sig") as file:
        df = json.load(file)
        print('????????????????????????aaaaaaaaaaaaaaa')
        print(type(df))
        print(df[0])
        print()

        csv_url = os.getcwd() + "\movies\\fixtures\movies.csv"
        # field names  
        fields = ['id', 'title', 'original_title', 'release_date', 'vote_average', 'popularity', 'overview', 'backdrop_path', 'poster_path', 'genres', 'keywords', 'actors', 'directors', 'vote_average_naver', 'link_naver']  
        
        # ?????? ????????? ?????? ??????
        # m = df['vote_average'].quantile(0.9)
        # print('mmmmmmmm', m)
        # print()

        # df = df.loc[df['vote_average'] >= m]
        # c = df['vote_average'].mean()

        # data rows of csv file  
        rows = [user_row]

        for i in range(1000):
            data = []

            # ?????? ?????????
            # m = df[i]['fields']['vote_average']
            # data
            data.append(df[i]['pk'])
            data.append(df[i]['fields']['title']) #
            data.append(df[i]['fields']['original_title']) #
            data.append(df[i]['fields']['release_date']) #
            data.append(df[i]['fields']['vote_average']) #
            data.append(df[i]['fields']['popularity'])
            data.append(df[i]['fields']['overview']) #
            data.append(df[i]['fields']['backdrop_path']) #
            data.append(df[i]['fields']['poster_path']) #
            data.append(df[i]['fields']['genres']) 
            data.append(df[i]['fields']['keywords']) #
            data.append(df[i]['fields']['actors'])
            data.append(df[i]['fields']['directors'])
            if df[i]['fields'].get('vote_average_naver', False):
                data.append(df[i]['fields']['vote_average_naver'])
                data.append(df[i]['fields']['link_naver'])
            rows.append(data)

        with open(csv_url, 'w', newline='', encoding="utf-8-sig") as f: 
            # using csv.writer method from CSV package 
            write = csv.writer(f) 
            
            write.writerow(fields)
            write.writerows(rows)


