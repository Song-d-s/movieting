import requests
import json
from datetime import datetime
import re

# papago
import os
import sys
import urllib.request

# google trans
from googletrans import Translator
translator = Translator()
import time

# 키 값 입력
TMDB_KEY = "" # TMDB에서 발급받은 키 값
NVR_ID = ""
NVR_SECRET = ""

NUM_OF_MOVIES = 1000
print('시작', NUM_OF_MOVIES)

# with open('./movie_db.json', 'w', encoding='UTF-8') as f:
#     response = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_KEY}&language=ko-KR&page=1').text
#     json_data = json.loads(response)
#     # print(json_data)
#     json.dump(json_data, f, indent=4, ensure_ascii=False)

# with open('./movie_db.json', 'r', encoding='UTF-8') as f:
#     data = json.load(f)
#     print(len(data["results"]))
#     movies = data["results"]
#     for movie in movies:
#         print(movie["id"])

def papagoTrans(text):
    # print(text)
    client_id = NVR_ID # 개발자센터에서 발급받은 Client ID 값
    client_secret = NVR_SECRET # 개발자센터에서 발급받은 Client Secret 값
    encText = urllib.parse.quote(text)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        res = json.loads(response_body.decode('utf-8'))
        return res['message']['result']['translatedText']
    else:
        print("Papago Error Code:" + rescode)
        return text

def isKorean(text):
    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')  
    result = hangul.findall(text)
    return len(result)

def prod_movie_json():
    data_index = set()
    data_refined = []
    keywords_refined = []
    keywords_index = set()
    actors_refined = []
    directors_refined = []
    for page in range(1, 1000):
        print(f'running on page {page}')
        response = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_KEY}&language=ko-KR&page={page}').json()
        movies = response["results"]
        for movie in movies:
            if movie['id'] in data_index:
                print('error: 중복 영화')
                continue
            if movie.get('release_date', '') == '':
                print('error: 날짜 없음')
                continue
            if movie.get('title', '') == '':
                print('error: 제목 없음', movie['title'], movie['original_title'])
                continue
            if movie.get('overview', '') == '':
                print('error: 내용 없음')
                continue
            if movie.get('original_language', '') == 'zh-CN':
                print('skip: 중국영화')
                continue

            only_latest = datetime.strptime(movie['release_date'], '%Y-%m-%d') > datetime.strptime('2012-11-10', '%Y-%m-%d')
            if movie.get('vote_average', 0) > 5 and movie.get('backdrop_path', False) and movie.get('poster_path', False) and only_latest and isKorean(movie['title']):
                # from pop movies
                fields = {
                    'title': movie['title'],
                    'original_title': movie['original_title'],
                    'release_date': movie['release_date'],
                    'vote_average': movie['vote_average'],
                    'vote_count' : movie['vote_count'],
                    'popularity' : movie['popularity'],
                    'overview': movie['overview'],
                    'backdrop_path': movie['backdrop_path'],
                    'poster_path': movie['poster_path'],
                    'genres': movie['genre_ids'],
                }

                # add video
                response = requests.get(f'https://api.themoviedb.org/3/movie/{movie["id"]}/videos?api_key={TMDB_KEY}&language=ko-KR')
                if response:
                    response = response.json()
                    videos = response['results']
                    youtube = []
                    for each in videos:
                        if each['site'] == 'YouTube' and each['official'] and each['type'] == 'Trailer':
                            youtube.append(each["key"])
                    if len(youtube):
                        fields['youtube'] = youtube[0]

                # add keyword
                response = requests.get(f'https://api.themoviedb.org/3/movie/{movie["id"]}/keywords?api_key={TMDB_KEY}').json()
                keywords = response['keywords']
                if len(keywords) == 0:
                    print('error: 키워드 없음')
                    continue
                keywords_id = []
                for keyword in keywords:
                    keywords_id.append(keyword['id'])

                    # prod keyword json
                    if keyword['id'] in keywords_index:
                        print(f'중복 키워드 {keyword["id"]}')
                        continue
                    keywords_index.add(keyword['id'])

                    translated = ''
                    while translated=='':
                        try:
                            translated = translator.translate(keyword['name'], src='en', dest='ko').text
                        except:
                            print('error: 번역 실패')
                            time.sleep(1)
                            pass

                    keyword_fields = {
                        'id' : keyword['id'],
                        'name' : translated,
                    }

                    keyword_data = {
                        'pk': keyword['id'],
                        'model': 'movies.keyword',
                        'fields': keyword_fields,
                    }
                    keywords_refined.append(keyword_data)
                # movie - keywords 입력
                fields['keywords'] = keywords_id

                # director and actors
                response = requests.get(f'https://api.themoviedb.org/3/movie/{movie["id"]}/credits?api_key={TMDB_KEY}&language=ko-KR').json()
                # actors
                actors = response['cast']
                actors_id = []
                # 5 actors from the 0
                n = 5
                if len(actors) < n: n = len(actors)
                for i in range(0, n):
                    actor = actors[i]
                    actors_id.append(actor['id'])

                    actor_fields = {
                        'id' : actor['id'],
                        'name' : actor['name'],
                        'profile_path' : actor['profile_path'],
                    }
                    actor_data = {
                        'pk': actor['id'],
                        'model': 'movies.actor',
                        'fields': actor_fields,
                    }
                    if actor_data not in actors_refined:
                        actors_refined.append(actor_data)
                fields['actors'] = actors_id
                # director
                crews = response['crew']
                directors_id = []
                for crew in crews:
                    if crew['job'] == 'Director':
                        directors_id.append(crew['id'])

                        director_fields = {
                            'id' : crew['id'],
                            'name' : crew['name'],
                            'profile_path' : crew['profile_path'],
                        }
                        director_data = {
                            'pk': crew['id'],
                            'model': 'movies.director',
                            'fields': director_fields,
                        }
                        if director_data not in directors_refined:
                            directors_refined.append(director_data)
                fields['directors'] = directors_id

                # add naver rating
                # X-Naver-Client-Id
                # X-Naver-Client-Secret
                NAVER_ID = NVR_ID   # 발급받은 키 값
                NAVER_SECRET = NVR_SECRET
                # query
                Q = movie['original_title']
                response = requests.get(f'https://openapi.naver.com/v1/search/movie.json?query={Q}', headers= {'X-Naver-Client-Id':NAVER_ID, 'X-Naver-Client-Secret':NAVER_SECRET}).json()
                if response.get('items', False):
                    first_res = response['items'][0]
                    fields['vote_average_naver'] = first_res['userRating']
                    fields['link_naver'] = first_res['link']

                data = {
                    'pk': movie['id'],
                    'model': 'movies.movie',
                    'fields': fields,
                }

                data_index.add(movie['id'])
                data_refined.append(data)
                print('success',movie['id'], '추가', f'({len(data_refined)}/{NUM_OF_MOVIES})')
            
            # prod JSON
            if len(data_refined) >= NUM_OF_MOVIES:
                print(len(data_refined), '개 생성')
                with open('./movies.json', 'w', encoding='UTF-8') as f:
                    json.dump(data_refined, f, indent=4, ensure_ascii=False)
                with open('./keywords.json', 'w', encoding='UTF-8') as f:
                    json.dump(keywords_refined, f, indent=4, ensure_ascii=False)
                with open('./actors.json', 'w', encoding='UTF-8') as f:
                    json.dump(actors_refined, f, indent=4, ensure_ascii=False)
                with open('./directors.json', 'w', encoding='UTF-8') as f:
                    json.dump(directors_refined, f, indent=4, ensure_ascii=False)
                return


def prod_genre_json():
    data_refined = []
    response = requests.get(f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_KEY}&language=ko-KR').json()
    genres = response['genres']
    # print(genres)
    for genre in genres:
        fields = {
            'id': genre['id'],
            'name': genre['name']
        }
        
        data = {
            'pk': genre['id'],
            'model': 'movies.genre',
            'fields': fields,
        }

        data_refined.append(data)

    with open('./genres.json', 'w', encoding='UTF-8') as f:
        json.dump(data_refined, f, indent=4, ensure_ascii=False)
    return



prod_movie_json()
# prod_genre_json()