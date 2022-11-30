from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse  
from .serializers import UserSerializer
from .models import User
from movies.models import Movie, Comment
import jwt
import json
import requests
import pandas as pd
import math
import numpy as np
import operator
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def kakaoLoginView(request):
    access_token = request.data['res']['access_token']
    url = 'https://kapi.kakao.com/v2/user/me'    
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'Content-type' : 'application/x-www-form-urlencoded; charset=utf-8'
    }

    kakao_response = requests.get(url, headers=headers)
    kakao_response = json.loads(kakao_response.text)

    # kakao_id 로 검색해보고, 
    user = User.objects.filter(id=kakao_response['id'])
    if user:
        # 있으면 로그인 진행
        serializer = UserSerializer(instance=user[0])
        data = {
            'serializer' : serializer.data,
            'access' : access_token
        }
        res = Response(data, status=status.HTTP_200_OK)
        return res


    # 없으면 회원가입 진행
    print('없음 -> 회원가입 진행')
    print(kakao_response)
    user_data = {
        'id':kakao_response['id'],
        'username':kakao_response['properties']['nickname'],
        'email':kakao_response['kakao_account']['email'],
        'password':str(kakao_response['id']),
        'gender':kakao_response['kakao_account']['gender'],
        'imgUrl':kakao_response['kakao_account']['profile']['profile_image_url'],
        # 'followings' : [],
    }
    
    serializer = UserSerializer(data=user_data)
    print()
    print(serializer)
    print()
    if serializer.is_valid(raise_exception=True):
        users = serializer.save()
        password = str(kakao_response['id'])
        users.set_password(password)
        users.save()
        data = {
            'serializer' : serializer.data,
            'access' : access_token
        }
        result = Response(data, status=status.HTTP_201_CREATED)
        return result
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def mypage(request):
    print('마이페이지in')
    
    if request.user.is_authenticated:
        print('is_authenticated')
        print()

        # 사용자가 좋아요 누른 영화 목록
        movies = User.objects.filter(id=request.user.id)[0].like_movies.all().values()

        # 사용자가 작성한 리뷰
        comments = Comment.objects.filter(user_id=request.user.id).filter(is_survey=0).values()

        # 사용자의 팔로워
        followers = User.objects.filter(id=request.user.id)[0].followers.all().values()
        
        data = {
            'user_like_movies' : movies,
            'user_like_movies_len' : len(movies),
            'user_created_comments' : comments,
            'user_created_comments_len' : len(comments),
            'followers' : followers,
            'followers_len' : len(followers),
        }
        return Response(data)

    print('is_authenticated x')
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def userpage(request, user_id):
    print('userPage in 💛')
    print(user_id)
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(instance=user)

    # 사용자가 좋아요 누른 영화 목록
    movies = User.objects.filter(id=user_id)[0].like_movies.all().values()

    # 사용자가 작성한 리뷰
    comments = Comment.objects.filter(user_id=user_id).filter(is_survey=0).values()

    serializer.data['user_like_movies'] = movies
    serializer.data['user_created_comments'] = comments

    print(user)
    data = {
        'username' : user.username,
        'email' : user.email,
        'gender' : user.gender,
        'imgUrl' : user.imgUrl,
        'user_like_movies' : movies,
        'user_like_movies_len' : len(movies),
        'user_created_comments' : comments,
        'user_created_comments_len' : len(comments),
    }

    return Response(data)


@api_view(['POST'])
def follow(request, user_pk):
    if request.user.is_authenticated:
        # User = get_user_model()
        me = request.user
        you = User.objects.get(pk=user_pk)
        # 자기 자신 팔로우 금지
        if me != you:
            # 내(request.user)가 그 사람의 팔로워 목록에 있다면
            # 1. if me in you.followers.all():
            # 2. exists() : DTL에서는 괄호를 쓸 수 없어서 이건 html에서는 못쓴다.
            if you.followers.filter(pk=me.pk).exists():
            # 언팔로우
                you.followers.remove(me)
            else:
            # 팔로우
                you.followers.add(me)
        
        serializer = UserSerializer(instance=me)
    return Response(serializer.data)
    # return Response('accounts:login')


@api_view(['POST'])
def user_similarity_start(request):

    user_id = request.user.id

    ratings_expand = {}

    comments = Comment.objects.all().values()
    for x in comments:
        if x['user_id'] in ratings_expand.keys():
            ratings_expand[x['user_id']][x['movie_id']] = x['rating']
        else:
            ratings_expand[x['user_id']] = {
                x['movie_id'] : x['rating']
            }

    dataframe = pd.DataFrame(ratings_expand).T

    print(ratings_expand)

    movies = []
    for i in dataframe.loc[user_id,:].index:
        if math.isnan(dataframe.loc[user_id,i]) == False:
            movies.append(i)
    
    # U_df는 name 사용자가 평가한 것만 추출합니다.
    U_df = pd.DataFrame(dataframe.loc[user_id,movies] ).T
    
    # other_df는 name 사용자를 제외한 데이터프레임입니다.
    other_df=dataframe.loc[:,movies].drop(user_id, axis=0)
    
    #U_list는 name 사용자가 평가한 영화(str)를 리스트에 담습니다.
    U_list= list(U_df.index)
    
    #sum_dict에 name과 다른 사용자 간의 유사도를 평가한 결과를 담게 됩니다.
    sim_dict={}
    
    
    # user와 name 사용자 둘 다 평점을 매긴 영화에 대한 벡터로 코사인 유사도를 구합니다.
    for user in other_df.index:
        sm= [m for m in U_df.columns if math.isnan(other_df.loc[user,m])==False]
        
        main_n = np.linalg.norm(U_df.loc[user_id,sm])
        user_n = np.linalg.norm(other_df.loc[user,sm])
        prod = np.dot(U_df.loc[user_id,sm], other_df.loc[user,sm])
        sim_dict[user]=prod/(main_n*user_n)
    
    print()
    print(sim_dict)
    print()

    result = sorted(sim_dict.items() ,key=operator.itemgetter(1), reverse=True)[:2]

    ids = []
    for y in result:
        print(y[0])
        ids.append(y[0])

    users = User.objects.filter(id__in=ids)
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)

