from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.kakaoLoginView),
    path('mypage/', views.mypage),
    path('user/<int:user_id>/', views.userpage),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('usersimilarity/', views.user_similarity_start, name='usersimilarity'),
]